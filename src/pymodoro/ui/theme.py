# src/pymodoro/ui/theme.py
from dataclasses import dataclass
from pymodoro.timer import SessionType

# ASCII Art Constants
TOMATO_ART = """
             [bold green]▒▒[/bold green]
      [bold green]▒▒[/bold green]     [bold green]▒▒[/bold green]    [bold green]▒▒[/bold green]
        [bold green]▒▒[/bold green][red]██[/red][bold green]▒▒[/bold green][red]██[/red][bold green]▒▒▒▒[/bold green]
    [red]████▒▒▒▒▒▒▒▒[/red][dark_orange]▓▓[/dark_orange][red]▒▒████[/red]
  [red]██▒▒▒▒▒▒▒▒[/red][dark_orange]▓▓▓▓[/dark_orange][red]▒▒▒▒▒▒▒▒██[/red]
  [red]██▒▒▒▒▒▒▒▒▒▒▒▒▒▒    ▒▒██[/red]
[red]██[/red][dark_orange]▓▓[/dark_orange][red]▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒  ▒▒▒▒██[/red]
[red]██[/red][dark_orange]▓▓[/dark_orange][red]▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒  ▒▒██[/red]
[red]██[/red][dark_orange]▓▓[/dark_orange][red]▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██[/red]
[red]██[/red][dark_orange]▓▓▓▓[/dark_orange][red]▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██[/red]
  [red]██[/red][dark_orange]▓▓▓▓[/dark_orange][red]▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██[/red]
  [red]██[/red][dark_orange]▓▓▓▓▓▓▓▓▓▓[/dark_orange][red]▒▒▒▒▒▒▒▒▒▒██[/red]
    [red]████[/red][dark_orange]▓▓▓▓▓▓▓▓▓▓▓▓[/dark_orange][red]████[/red]
        [dark_orange]████████████[/dark_orange]
"""

BREAK_TOMATO_ART = """
             [bold green]▒▒[/bold green]
      [bold green]▒▒[/bold green]     [bold green]▒▒[/bold green]    [bold green]▒▒[/bold green]
        [bold green]▒▒[/bold green][green]██[/green][bold green]▒▒[/bold green][green]██[/green][bold green]▒▒▒▒[/bold green]
    [green]████▒▒▒▒▒▒▒▒[/green][dark_green]▓▓[/dark_green][green]▒▒████[/green]
  [green]██▒▒▒▒▒▒▒▒[/green][dark_green]▓▓▓▓[/dark_green][green]▒▒▒▒▒▒▒▒██[/green]
  [green]██▒▒▒▒▒▒▒▒▒▒▒▒▒▒    ▒▒██[/green]
[green]██[/green][dark_green]▓▓[/dark_green][green]▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒  ▒▒▒▒██[/green]
[green]██[/green][dark_green]▓▓[/dark_green][green]▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒  ▒▒██[/green]
[green]██[/green][dark_green]▓▓[/dark_green][green]▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██[/green]
[green]██[/green][dark_green]▓▓▓▓[/dark_green][green]▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██[/green]
  [green]██[/green][dark_green]▓▓▓▓[/dark_green][green]▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██[/green]
  [green]██[/green][dark_green]▓▓▓▓▓▓▓▓▓▓[/dark_green][green]▒▒▒▒▒▒▒▒▒▒██[/green]
    [green]████[/green][dark_green]▓▓▓▓▓▓▓▓▓▓▓▓[/dark_green][green]████[/green]
        [dark_green]████████████[/dark_green]
"""


PAUSE_TOMATO_ART = """
             [bold green]▒▒[/bold green]
      [bold green]▒▒[/bold green]     [bold green]▒▒[/bold green]    [bold green]▒▒[/bold green]
        [bold green]▒▒[/bold green][yellow]██[/yellow][bold green]▒▒[/bold green][yellow]██[/yellow][bold green]▒▒▒▒[/bold green]
    [yellow]████▒▒▒▒▒▒▒▒[/yellow][dark_orange]▓▓[/dark_orange][yellow]▒▒████[/yellow]
  [yellow]██▒▒▒▒▒▒▒▒[/yellow][dark_orange]▓▓▓▓[/dark_orange][yellow]▒▒▒▒▒▒▒▒██[/yellow]
  [yellow]██▒▒▒▒▒▒▒▒▒▒▒▒▒▒    ▒▒██[/yellow]
[yellow]██[/yellow][dark_orange]▓▓[/dark_orange][yellow]▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒  ▒▒▒▒██[/yellow]
[yellow]██[/yellow][dark_orange]▓▓[/dark_orange][yellow]▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒  ▒▒██[/yellow]
[yellow]██[/yellow][dark_orange]▓▓[/dark_orange][yellow]▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██[/yellow]
[yellow]██[/yellow][dark_orange]▓▓▓▓[/dark_orange][yellow]▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██[/yellow]
  [yellow]██[/yellow][dark_orange]▓▓▓▓[/dark_orange][yellow]▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██[/yellow]
  [yellow]██[/yellow][dark_orange]▓▓▓▓▓▓▓▓▓▓[/dark_orange][yellow]▒▒▒▒▒▒▒▒▒▒██[/yellow]
    [yellow]████[/yellow][dark_orange]▓▓▓▓▓▓▓▓▓▓▓▓[/dark_orange][yellow]████[/yellow]
        [dark_orange]████████████[/dark_orange]
"""

@dataclass
class SessionTheme:
    """Theme configuration for a session type."""
    primary_color: str
    icon: str
    session_name: str
    short_name: str
    art: str

@dataclass
class Dimensions:
    """UI dimension constants."""
    timer_panel_width: int = 12
    progress_bar_width: int = 40
    dialog_width: int = 60
    help_width: int = 65
    table_min_width: int = 50

# Session themes
THEMES = {
    SessionType.WORK: SessionTheme(
        primary_color="red",
        icon="🍅",
        session_name="Work Session",
        short_name="Work",
        art=TOMATO_ART
    ),
    SessionType.SHORT_BREAK: SessionTheme(
        primary_color="green",
        icon="☕",
        session_name="Short Break",
        short_name="Short Break", 
        art=BREAK_TOMATO_ART
    ),
    SessionType.LONG_BREAK: SessionTheme(
        primary_color="cyan",
        icon="☕",
        session_name="Long Break",
        short_name="Long Break", 
        art=BREAK_TOMATO_ART
    )
}

class ThemeManager:
    """Manages theme selection based on timer state."""
    
    def __init__(self):
        self.dimensions = Dimensions()
    
    def get_theme(self, session_type: SessionType, is_paused: bool = False) -> SessionTheme:
        """Get the appropriate theme for current session state."""
        theme = THEMES.get(session_type, THEMES[SessionType.WORK])
        
        if is_paused:
            # Return paused variant
            return SessionTheme(
                primary_color=theme.primary_color,
                icon=theme.icon,
                session_name=theme.session_name,
                short_name=theme.short_name,
                art=PAUSE_TOMATO_ART
            )
        
        return theme
    
    def get_display_color(self, session_type: SessionType, is_paused: bool = False) -> str:
        """Get the color to use for UI elements."""
        if is_paused:
            return "yellow"
        return THEMES.get(session_type, THEMES[SessionType.WORK]).primary_color