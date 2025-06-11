# src/pymodoro/interface.py
from rich.console import Console
from pymodoro.ui.screens import ScreenManager

console = Console()

class PomodoroUI:
    def __init__(self, timer):
        self.timer = timer
        self.screen_manager = ScreenManager()
        self._cache = {}
    
    def get_renderable(self, confirmation_type=None):
        """Get the current screen renderable."""
        # Extract timer state
        session_type = self.timer.current_session
        time_left = self.timer.time_left
        total_time = self.timer.settings[session_type]
        pomodoros_completed = self.timer.pomodoros_completed
        is_paused = not self.timer.is_running
        is_muted = self.timer.is_muted
        
        # Create cache key based on meaningful state
        cache_key = (
            session_type,
            pomodoros_completed,
            is_paused,
            is_muted,
            int(time_left),  # Round to seconds
            confirmation_type
        )
        
        # Check cache
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        # Get screen from screen manager
        if confirmation_type:
            screen = self.screen_manager.get_screen(
                confirmation_type,
                session_type=session_type,
                time_left=time_left,
                pomodoros_completed=pomodoros_completed,
                is_paused=is_paused,
                is_muted=is_muted
            )
        else:
            screen = self.screen_manager.get_screen(
                'main',
                session_type=session_type,
                time_left=time_left,
                total_time=total_time,
                pomodoros_completed=pomodoros_completed,
                is_paused=is_paused,
                is_muted=is_muted
            )
        
        # Cache the result
        self._cache = {cache_key: screen}  # Clear old cache entries
        
        return screen