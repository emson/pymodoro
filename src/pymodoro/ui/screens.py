# src/pymodoro/ui/screens.py
from abc import ABC, abstractmethod
from typing import Any
from pymodoro.timer import SessionType
from pymodoro.ui.theme import ThemeManager
from pymodoro.ui.components import TimerDisplay, ProgressBar, Header, ArtDisplay, Dialog
from pymodoro.ui.layout import LayoutGrid, Alignment, Spacing

class Screen(ABC):
    """Abstract base class for all screens."""
    
    @abstractmethod
    def render(self, **kwargs) -> Any:
        """Render the screen content."""
        pass

class MainScreen(Screen):
    """Primary timer interface using components."""
    
    def __init__(self, theme_manager: ThemeManager):
        self.theme_manager = theme_manager
        self.timer_display = TimerDisplay(theme_manager.dimensions)
        self.progress_bar = ProgressBar(theme_manager.dimensions)
        self.header = Header()
        self.art_display = ArtDisplay()
    
    def render(self, session_type: SessionType, time_left: float, total_time: float, 
              pomodoros_completed: int, is_paused: bool, is_muted: bool = False) -> Any:
        """Render the main timer screen."""
        # Get theme and display color
        theme = self.theme_manager.get_theme(session_type, is_paused)
        display_color = self.theme_manager.get_display_color(session_type, is_paused)
        
        # Create all components
        header = self.header.render(theme, pomodoros_completed, is_paused, display_color, is_muted)
        art = self.art_display.render(theme.art)
        timer = self.timer_display.render(time_left, display_color)
        
        # Use cyan progress bar for Long Break, otherwise use display_color
        progress_color = "cyan" if session_type == SessionType.LONG_BREAK else display_color
        progress = self.progress_bar.render(time_left, total_time, progress_color)
        help_text = Spacing.create_help_text()
        
        # Create layout
        table = LayoutGrid.create_main_layout(self.theme_manager.dimensions.table_min_width)
        
        # Add components with consistent spacing
        LayoutGrid.add_component(table, header)
        LayoutGrid.add_spacer(table)
        LayoutGrid.add_component(table, Alignment.center_horizontal(art))
        LayoutGrid.add_component(table, Alignment.center_horizontal(timer))
        LayoutGrid.add_spacer(table)
        LayoutGrid.add_component(table, Alignment.center_horizontal(progress))
        LayoutGrid.add_spacer(table)
        LayoutGrid.add_spacer(table)
        LayoutGrid.add_component(table, help_text)
        
        return Alignment.center_vertical_and_horizontal(table)

class HelpScreen(Screen):
    """Help overlay screen."""
    
    def __init__(self, theme_manager: ThemeManager):
        self.theme_manager = theme_manager
        self.dialog = Dialog(theme_manager.dimensions)
    
    def render(self, session_type: SessionType, time_left: float, pomodoros_completed: int, is_paused: bool, is_muted: bool = False) -> Any:
        """Render the help screen."""
        theme = self.theme_manager.get_theme(session_type, is_paused)
        display_color = self.theme_manager.get_display_color(session_type, is_paused)
        
        help_panel = self.dialog.render_help(theme, time_left, pomodoros_completed, is_paused, display_color)
        return Alignment.center_vertical_and_horizontal(help_panel)

class ConfirmationScreen(Screen):
    """Modal confirmation dialogs."""
    
    def __init__(self, theme_manager: ThemeManager):
        self.theme_manager = theme_manager
        self.dialog = Dialog(theme_manager.dimensions)
    
    def render(self, confirmation_type: str, session_type: SessionType, time_left: float, 
              pomodoros_completed: int, is_paused: bool, is_muted: bool = False) -> Any:
        """Render a confirmation dialog."""
        theme = self.theme_manager.get_theme(session_type, is_paused)
        display_color = self.theme_manager.get_display_color(session_type, is_paused)
        
        confirmation_panel = self.dialog.render_confirmation(
            confirmation_type, theme, time_left, pomodoros_completed, display_color, is_muted
        )
        return Alignment.center_vertical_and_horizontal(confirmation_panel)

class ScreenManager:
    """Coordinate screen transitions and overlay management."""
    
    def __init__(self):
        self.theme_manager = ThemeManager()
        self.main_screen = MainScreen(self.theme_manager)
        self.help_screen = HelpScreen(self.theme_manager)
        self.confirmation_screen = ConfirmationScreen(self.theme_manager)
    
    def get_screen(self, screen_type: str, **kwargs) -> Any:
        """Get the appropriate screen based on type."""
        if screen_type == 'help':
            return self.help_screen.render(**kwargs)
        elif screen_type in ['skip', 'reset', 'quit']:
            return self.confirmation_screen.render(confirmation_type=screen_type, **kwargs)
        else:  # main screen
            return self.main_screen.render(**kwargs)