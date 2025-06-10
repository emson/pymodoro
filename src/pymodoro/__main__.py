# src/pymodoro/__main__.py
import time
import argparse
from rich.live import Live

from .timer import PomodoroTimer, SessionType
from .interface import PomodoroUI, console
from .keyboard import TerminalKeyboard
from .sound import play_work_end, play_break_end, play_warning

def main():
    parser = argparse.ArgumentParser(
        description="🍅 Pymodoro - A beautiful command-line Pomodoro timer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
KEYBOARD CONTROLS (during runtime):
  SPACE         Pause/Resume the current session
  N             Skip to next session (with confirmation)
  R             Reset current session to beginning (with confirmation)
  Q             Quit the application (with confirmation)

ABOUT THE POMODORO TECHNIQUE:
  The Pomodoro Technique is a time management method that uses a timer to break
  work into intervals (traditionally 25 minutes) separated by short breaks.
  After 4 work sessions, take a longer break.

EXAMPLES:
  pymodoro                           # Default: 25min work, 5min short break, 15min long break
  pymodoro -w 45                     # 45-minute work sessions
  pymodoro -w 25 -s 5 -l 30          # Custom durations for all session types
  pymodoro --work 50 --short 10      # Longer work sessions with longer short breaks
  pymodoro -n 2                      # Warning sound 2 minutes before session end
  pymodoro --notify 3                # Warning sound 3 minutes before session end

FEATURES:
  • Beautiful terminal UI with session-aware colors
  • Visual progress bar and timer display
  • Audio notifications at session transitions
  • Configurable warning sound before session ends
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
    
    # Add version information
    parser.add_argument(
        "--version", 
        action="version", 
        version="Pymodoro 0.1.0"
    )
    
    args = parser.parse_args()

    timer = PomodoroTimer(args.work, args.short, args.long, args.notify)
    ui = PomodoroUI(timer)
    
    timer.start() # Start the timer initially

    try:
        with TerminalKeyboard() as kb, Live(ui.get_renderable(), screen=True, redirect_stderr=False, refresh_per_second=10) as live:
            should_exit = False
            confirmation_state = None  # None, 'skip', 'reset', or 'quit'
            
            while not should_exit:
                key = kb.getch()
                if key:
                    if confirmation_state:
                        # Handle confirmation responses
                        if key.lower() == 'y':
                            if confirmation_state == 'skip':
                                # Execute skip action - update timer first, then play sound
                                current_session_type = timer.current_session
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
                        elif key.lower() == 'n' or key == ' ':  # N or spacebar cancels
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
                
                time.sleep(0.1)
                
                # Check for warning before checking session change
                if timer.should_play_warning():
                    play_warning()
                
                session_changed = timer.tick()
                if session_changed:
                    if timer.current_session == SessionType.WORK:
                        play_break_end() # Sound for break ending
                    else:
                        play_work_end() # Sound for work ending
                
                # Update display - show confirmation overlay if needed
                if confirmation_state:
                    live.update(ui.get_renderable(confirmation_state))
                else:
                    live.update(ui.get_renderable())
    finally:
        console.print("[bold green]🍅 Pymodoro finished. Great work![/bold green]")

if __name__ == "__main__":
    main()
