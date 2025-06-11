# src/pymodoro/__main__.py
import time
import argparse
from rich.live import Live

from .timer import PomodoroTimer, SessionType
from .interface import PomodoroUI, console
from .keyboard import TerminalKeyboard
from .sound import play_work_end, play_break_end, play_warning
from .storage import load_or_initialize_day_log, add_session, reset_today_log, open_log_in_editor

def main():
    parser = argparse.ArgumentParser(
        description="🍅 Pymodoro - A beautiful command-line Pomodoro timer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
KEYBOARD CONTROLS (during runtime):
  SPACE         Pause/Resume the current session
  n             Skip to next session (with confirmation)
  r             Reset current session to beginning (with confirmation)
  q             Quit the application (with confirmation)
  h             Show help screen

ABOUT THE POMODORO TECHNIQUE:
  The Pomodoro Technique is a time management method that uses a timer to break
  work into intervals (traditionally 25 minutes) separated by short breaks.
  After a configurable number of work sessions, take a longer break.

EXAMPLES:
  pymodoro                           # Default: 25min work, 5min short break, 15min long break
  pymodoro -w 45                     # 45-minute work sessions
  pymodoro -w 25 -s 5 -l 30          # Custom durations for all session types
  pymodoro --work 50 --short 10      # Longer work sessions with longer short breaks
  pymodoro -n 2                      # Warning sound 2 minutes before session end
  pymodoro --notify 3                # Warning sound 3 minutes before session end
  pymodoro -f 2                      # Long break after every 2 work sessions
  pymodoro --frequency 6             # Long break after every 6 work sessions
  pymodoro -w 30 -f 3                # 30-minute work sessions, long break every 3 sessions

FEATURES:
  • Beautiful terminal UI with session-aware colors
  • Visual progress bar and timer display
  • Audio notifications at session transitions
  • Configurable warning sound before session ends
  • Configurable long break frequency (1 to N work sessions)
  • Confirmation dialogs for destructive actions
  • Pomodoro counter to track completed work sessions
  • Pause/resume functionality
  • Skip sessions when needed

For more information about the Pomodoro Technique:
  https://en.wikipedia.org/wiki/Pomodoro_Technique
        """.strip()
    )
    
    parser.add_argument(
        "-w", "--work", 
        type=int, 
        default=25, 
        metavar="MINUTES",
        help="Duration of work sessions in minutes (default: 25)"
    )
    parser.add_argument(
        "-s", "--short", 
        type=int, 
        default=5, 
        metavar="MINUTES",
        help="Duration of short breaks in minutes (default: 5)"
    )
    parser.add_argument(
        "-l", "--long", 
        type=int, 
        default=15, 
        metavar="MINUTES",
        help="Duration of long breaks in minutes (default: 15)"
    )
    parser.add_argument(
        "-n", "--notify", 
        type=int, 
        default=1, 
        metavar="MINUTES",
        help="Play warning sound N minutes before session ends (default: 1)"
    )
    parser.add_argument(
        "-f", "--frequency", 
        type=int, 
        default=4, 
        metavar="COUNT",
        help="Number of work sessions before a long break (default: 4)"
    )
    
    # Add version information
    parser.add_argument(
        "--version", 
        action="version", 
        version="Pymodoro 0.1.0"
    )
    
    # Log management options
    parser.add_argument(
        "--reset_log",
        action="store_true",
        help="Reset today's session log to empty and exit"
    )
    parser.add_argument(
        "--open_log",
        action="store_true", 
        help="Open today's session log in default editor and exit"
    )
    
    args = parser.parse_args()

    # Handle log management actions (exit immediately after execution)
    if args.reset_log:
        reset_today_log()
        console.print("[green]✓[/green] Today's session log has been reset to empty")
        return
    
    if args.open_log:
        open_log_in_editor()
        console.print("[green]✓[/green] Opening today's session log in default editor")
        return

    # Validate frequency parameter
    if args.frequency < 1:
        parser.error("Long break frequency must be at least 1")

    # Load existing session data
    day_log = load_or_initialize_day_log()
    
    timer = PomodoroTimer(args.work, args.short, args.long, args.notify, args.frequency)
    timer.pomodoros_completed = day_log.session_count
    ui = PomodoroUI(timer)
    
    timer.start() # Start the timer initially

    try:
        with TerminalKeyboard() as kb, Live(ui.get_renderable(), screen=True, redirect_stderr=False, refresh_per_second=4) as live:
            should_exit = False
            confirmation_state = None  # None, 'skip', 'reset', 'quit', or 'help'
            
            while not should_exit:
                key = kb.getch()
                if key:
                    if confirmation_state:
                        # Handle confirmation/help screen responses
                        if confirmation_state == 'help':
                            # Any key dismisses help screen (except for action keys which should still work)
                            if key.lower() == 'h' or key == '\x1b':  # h or ESC explicitly close help
                                confirmation_state = None
                            elif key == ' ':
                                # Space should work normally (pause/resume) even from help
                                timer.toggle_pause()
                                confirmation_state = None
                            elif key.lower() == 'n':
                                # N should work normally (skip) even from help
                                confirmation_state = 'skip'
                            elif key.lower() == 'r':
                                # R should work normally (reset) even from help
                                confirmation_state = 'reset'
                            elif key.lower() == 'q':
                                # Q should work normally (quit) even from help
                                confirmation_state = 'quit'
                            else:
                                # Any other key dismisses help
                                confirmation_state = None
                        else:
                            # Handle normal confirmation responses (skip/reset/quit)
                            if key.lower() == 'y':
                                if confirmation_state == 'skip':
                                    # Execute skip action - update timer first, then play sound
                                    current_session_type = timer.current_session
                                    # If skipping a work session, save it first
                                    if current_session_type == SessionType.WORK:
                                        add_session(timer.settings[SessionType.WORK] // 60)
                                    timer.next_session(skip=True)
                                    # Play sound asynchronously after state change
                                    if current_session_type == SessionType.WORK:
                                        play_work_end()
                                    else:
                                        play_break_end()
                                elif confirmation_state == 'reset':
                                    # Execute reset action
                                    timer.reset()
                                elif confirmation_state == 'quit':
                                    # Execute quit action
                                    should_exit = True
                                confirmation_state = None
                            elif key.lower() == 'n' or key == ' ' or key == '\x1b':  # N, spacebar, or ESC cancels
                                confirmation_state = None
                    else:
                        # Handle normal key presses
                        if key == ' ':
                            timer.toggle_pause()
                        elif key.lower() == 'n':
                            confirmation_state = 'skip'
                        elif key.lower() == 'r':
                            confirmation_state = 'reset'
                        elif key.lower() == 'q':
                            confirmation_state = 'quit'
                        elif key.lower() == 'h':
                            confirmation_state = 'help'
                
                time.sleep(0.1)
                
                # Check for warning before checking session change
                if timer.should_play_warning():
                    play_warning()
                
                session_changed = timer.tick()
                if session_changed:
                    if timer.current_session == SessionType.WORK:
                        play_break_end() # Sound for break ending
                    else:
                        # Work session completed - save it and play sound
                        add_session(timer.settings[SessionType.WORK] // 60)
                        play_work_end() # Sound for work ending
                
                # Update display with a freshly generated renderable
                # This is a key fix to prevent stale buffer issues in Rich Live
                new_renderable = ui.get_renderable(confirmation_state)
                live.update(new_renderable)
    finally:
        console.print("[bold green]🍅 Pymodoro finished. Great work![/bold green]")

if __name__ == "__main__":
    main()
