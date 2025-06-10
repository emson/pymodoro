# src/pymodoro/__main__.py
import time
import argparse
from rich.live import Live

from .timer import PomodoroTimer, SessionType
from .interface import PomodoroUI, console
from .keyboard import KeyboardListener
from .sound import play_work_end, play_break_end

# Global flag to signal exit
should_exit = False

def handle_key_press(key):
    global timer, should_exit
    if key == ' ':
        timer.toggle_pause()
    elif key.lower() == 'n':
        if timer.current_session == SessionType.WORK:
            play_work_end()
        else:
            play_break_end()
        timer.next_session(skip=True)
    elif key.lower() == 'q':
        should_exit = True

def main():
    global timer # Make timer accessible to the key handler

    parser = argparse.ArgumentParser(description="A beautiful command-line pomodoro timer.")
    parser.add_argument("-w", "--work", type=int, default=25, help="Work session duration in minutes.")
    parser.add_argument("-s", "--short", type=int, default=5, help="Short break duration in minutes.")
    parser.add_argument("-l", "--long", type=int, default=15, help="Long break duration in minutes.")
    args = parser.parse_args()

    timer = PomodoroTimer(args.work, args.short, args.long)
    ui = PomodoroUI(timer)
    
    kb_listener = KeyboardListener(handle_key_press)
    kb_listener.start()

    timer.start() # Start the timer initially

    try:
        with Live(ui.get_renderable(), screen=True, redirect_stderr=False, refresh_per_second=10) as live:
            while not should_exit:
                time.sleep(0.1)
                session_changed = timer.tick()
                if session_changed:
                    if timer.current_session == SessionType.WORK:
                        play_break_end() # Sound for break ending
                    else:
                        play_work_end() # Sound for work ending
                
                live.update(ui.get_renderable())
    finally:
        kb_listener.stop()
        console.print("[bold red]Pymodoro finished. Great work![/bold red]")

if __name__ == "__main__":
    main()
