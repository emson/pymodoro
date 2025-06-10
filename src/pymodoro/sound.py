# src/pymodoro/sound.py
import sys

def play_notification_sound():
    """
    Plays a simple system bell sound.
    This is the most cross-platform and dependency-free way to make a sound.
    It works on most terminal emulators on Linux, macOS, and Windows.
    We write to stderr to avoid interfering with the `rich` Live display on stdout.
    """
    sys.stderr.write("\a")
    sys.stderr.flush()

def play_work_end():
    """Plays a sound to signify the end of a work session."""
    play_notification_sound()

def play_break_end():
    """Plays a sound to signify the end of a break session."""
    play_notification_sound()
