# src/pymodoro/timer.py
import time
from enum import Enum, auto

class SessionType(Enum):
    WORK = auto()
    SHORT_BREAK = auto()
    LONG_BREAK = auto()

class PomodoroTimer:
    def __init__(self, work_mins=25, short_break_mins=5, long_break_mins=15, warning_mins=1, long_break_frequency=4):
        self.settings = {
            SessionType.WORK: work_mins * 60,
            SessionType.SHORT_BREAK: short_break_mins * 60,
            SessionType.LONG_BREAK: long_break_mins * 60,
        }
        self.current_session = SessionType.WORK
        self.time_left = self.settings[self.current_session]
        self.is_running = False
        self.pomodoros_completed = 0
        self.start_time = None
        self._last_tick_time = None
        self.warning_minutes = warning_mins
        self.long_break_frequency = long_break_frequency  # How many work sessions before long break
        self._warning_played = False  # Track if warning has been played for current session

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.start_time = time.monotonic()
            self._last_tick_time = self.start_time

    def pause(self):
        if self.is_running:
            self.is_running = False
            # Save the elapsed time when pausing
            self.time_left -= (time.monotonic() - self._last_tick_time)
            self.time_left = max(0, self.time_left)

    def resume(self):
        if not self.is_running:
            self.is_running = True
            self._last_tick_time = time.monotonic()

    def toggle_pause(self):
        if self.is_running:
            self.pause()
        else:
            self.resume()
    
    def reset(self):
        """Reset the current session timer to its full duration."""
        self.time_left = self.settings[self.current_session]
        self._last_tick_time = time.monotonic()
        self._warning_played = False  # Reset warning state on reset
        # Keep the timer running state as it was
    
    def should_play_warning(self) -> bool:
        """Check if warning should be played (only once per session)."""
        warning_threshold = self.warning_minutes * 60
        if (not self._warning_played and 
            self.is_running and 
            self.time_left <= warning_threshold and 
            self.time_left > 0):
            self._warning_played = True
            return True
        return False
    
    def tick(self):
        if not self.is_running:
            return False  # No change
        
        elapsed = time.monotonic() - self._last_tick_time
        self._last_tick_time = time.monotonic()
        self.time_left -= elapsed
        
        if self.time_left <= 0:
            self.next_session()
            return True # Session changed
        return False

    def next_session(self, skip=False):
        if self.current_session == SessionType.WORK:
            self.pomodoros_completed += 1
            if self.pomodoros_completed % self.long_break_frequency == 0:
                self.current_session = SessionType.LONG_BREAK
            else:
                self.current_session = SessionType.SHORT_BREAK
        else:
            self.current_session = SessionType.WORK
        
        self.time_left = self.settings[self.current_session]
        self._last_tick_time = time.monotonic()
        self._warning_played = False  # Reset warning state for new session
        # Ensure it's running when skipping to the next session
        if skip:
            self.is_running = True

