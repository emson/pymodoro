# src/pymodoro/keyboard.py
import sys
import termios
import tty
import select

class TerminalKeyboard:
    def __init__(self):
        self._original_settings = None

    def start(self):
        self._original_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())

    def stop(self):
        if self._original_settings:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self._original_settings)

    def getch(self):
        if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            return sys.stdin.read(1)
        return None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
