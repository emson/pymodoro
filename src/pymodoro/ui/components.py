# src/pymodoro/ui/components.py
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich.console import Group
from pymodoro.ui.theme import SessionTheme, Dimensions

class TimerDisplay:
    """Renders timer in MM:SS format with Rich Panel."""
    
    def __init__(self, dimensions: Dimensions):
        self.dimensions = dimensions
    
    def render(self, time_left: float, display_color: str) -> Panel:
        """Render timer display panel."""
        try:
            mins, secs = divmod(int(time_left), 60)
            time_str = f"{mins:02d}:{secs:02d}"
            timer_text = Text(time_str, justify="center", style="bold white on black")
            return Panel(timer_text, width=self.dimensions.timer_panel_width, style=display_color)
        except Exception:
            # Fallback for any rendering errors
            fallback_text = Text("00:00", justify="center", style="bold white on black")
            return Panel(fallback_text, width=self.dimensions.timer_panel_width, style="white")

class ProgressBar:
    """Renders horizontal progress visualization."""
    
    def __init__(self, dimensions: Dimensions):
        self.dimensions = dimensions
    
    def render(self, time_left: float, total_time: float, display_color: str) -> Group:
        """Render progress bar component."""
        try:
            remaining = max(0, time_left)
            completed = total_time - remaining
            progress_ratio = completed / total_time if total_time > 0 else 0
            
            filled_width = int(progress_ratio * self.dimensions.progress_bar_width)
            empty_width = self.dimensions.progress_bar_width - filled_width
            
            filled_blocks = "█" * filled_width
            empty_blocks = "░" * empty_width
            bar_text = filled_blocks + empty_blocks
            
            # Create two rows for thickness
            progress_bar1 = Text(bar_text, style=f"bold {display_color}")
            progress_bar2 = Text(bar_text, style=f"bold {display_color}")
            
            return Group(progress_bar1, progress_bar2)
        except Exception:
            # Fallback progress bar
            fallback_text = "░" * self.dimensions.progress_bar_width
            fallback_bar = Text(fallback_text, style="white")
            return Group(fallback_bar, fallback_bar)

class Header:
    """Renders session title, pomodoro number, and pause status."""
    
    def render(self, theme: SessionTheme, pomodoros_completed: int, is_paused: bool, display_color: str, is_muted: bool = False) -> Text:
        """Render header text component."""
        try:
            header = Text(no_wrap=True, justify="center")
            
            # For work sessions, show pomodoro number
            if theme.short_name == "Work":
                header.append(theme.icon, style=f"bold {display_color}")
                header.append(" ", style=f"bold {display_color}")
                header.append(f"Pomodoro #{pomodoros_completed + 1}", style=f"bold {display_color}")
            else:
                # For breaks, show the break type
                header.append(theme.icon, style=f"bold {display_color}")
                header.append(" ", style=f"bold {display_color}")
                header.append(theme.short_name, style=f"bold {display_color}")
            
            # Add status indicators
            status_added = False
            
            # Add paused indicator if needed
            if is_paused:
                header.append(" | ", style=f"bold {display_color}")
                header.append("PAUSED", style="bold yellow")
                status_added = True
            
            # Add muted indicator if needed
            if is_muted:
                separator = " | " if status_added else " | "
                header.append(separator, style=f"bold {display_color}")
                header.append("🔇 MUTED", style="bold dim")
            
            return header
        except Exception:
            # Fallback header
            return Text(f"{theme.icon} {theme.short_name}", justify="center", style="bold white")

class ArtDisplay:
    """Renders ASCII art based on session state."""
    
    def render(self, art: str) -> Text:
        """Render ASCII art component."""
        try:
            return Text.from_markup(art)
        except Exception:
            # Fallback art
            return Text("🍅", justify="center", style="bold red")

class Dialog:
    """Reusable modal dialog system."""
    
    def __init__(self, dimensions: Dimensions):
        self.dimensions = dimensions
    
    def render_help(self, theme: SessionTheme, time_left: float, pomodoros_completed: int, is_paused: bool, display_color: str) -> Panel:
        """Render help dialog."""
        try:
            # Create help table
            help_table = Table(show_header=False, box=None, padding=(0, 2))
            help_table.add_column("Key", style="bold cyan", width=8)
            help_table.add_column("Action", style="white")
            
            help_table.add_row("SPACE", "Pause/Resume the current session")
            help_table.add_row("m", "Mute/Unmute sounds")
            help_table.add_row("n", "Skip to next session (with confirmation)")
            help_table.add_row("r", "Reset current session (with confirmation)")
            help_table.add_row("q", "Quit application (with confirmation)")
            help_table.add_row("h", "Show/hide this help screen")
            help_table.add_row("", "")
            help_table.add_row("ESC", "Close this help screen")
            
            # Session context
            mins, secs = divmod(int(time_left), 60)
            time_str = f"{mins:02d}:{secs:02d}"
            
            session_text = f"{theme.session_name} - {time_str} remaining"
            if theme.short_name == "Work":
                status_text = f"Pomodoro #{pomodoros_completed + 1}"
            else:
                status_text = "Break Time"
            
            if is_paused:
                session_text += " (PAUSED)"
            
            context_text = Text(f"Current: {session_text}", style="dim", justify="center")
            status_display = Text(status_text, style=f"bold {display_color}", justify="center")
            
            help_content = Group(
                status_display,
                context_text,
                "",
                Text("KEYBOARD SHORTCUTS", style="bold white", justify="center"),
                "",
                help_table,
                "",
                Text("Press any key to close this help screen", style="dim", justify="center")
            )
            
            return Panel(
                help_content,
                border_style=f"bold {display_color}",
                padding=(2, 4),
                width=self.dimensions.help_width,
                title="[bold]🍅 Pymodoro Help[/bold]",
                title_align="center"
            )
        except Exception:
            # Fallback help dialog
            fallback_content = Text("Help screen unavailable", justify="center", style="white")
            return Panel(fallback_content, border_style="white", title="Help")
    
    def render_confirmation(self, confirmation_type: str, theme: SessionTheme, time_left: float, pomodoros_completed: int, display_color: str, is_muted: bool = False) -> Panel:
        """Render confirmation dialog."""
        try:
            # Create confirmation content
            if confirmation_type == 'skip':
                if theme.short_name == "Work":
                    title = "Skip Work Session?"
                    message = f"Skip current work session and start break?\nYou'll lose progress on Pomodoro #{pomodoros_completed + 1}."
                else:
                    title = "Skip Break?"
                    message = "Skip current break and start next work session?"
            elif confirmation_type == 'reset':
                if theme.short_name == "Work":
                    title = "Reset Work Session?"
                    message = f"Reset current work session to full duration?\nPomodoro #{pomodoros_completed + 1} will restart from the beginning."
                else:
                    title = f"Reset {theme.short_name}?"
                    message = f"Reset current {theme.session_name.lower()} to full duration?\nThe break will restart from the beginning."
            else:  # quit
                title = "Quit Pymodoro?"
                message = "Are you sure you want to quit?\nAll progress will be lost."
            
            # Session context
            mins, secs = divmod(int(time_left), 60)
            time_str = f"{mins:02d}:{secs:02d}"
            context = f"Current: {theme.session_name} - {time_str} remaining"
            
            # Create dialog content
            title_text = Text(title, style=f"bold {display_color}", justify="center")
            context_text = Text(context, style="dim", justify="center")
            message_text = Text(message, style="white", justify="center")
            options_text = Text("Y - Yes    N - No    SPACE/ESC - Cancel", style="bold white", justify="center")
            
            confirmation_content = Group(
                title_text,
                "",
                context_text,
                "",
                message_text,
                "",
                "",
                options_text
            )
            
            return Panel(
                confirmation_content,
                border_style=f"bold {display_color}",
                padding=(2, 4),
                width=self.dimensions.dialog_width,
                title="[bold]Confirmation Required[/bold]",
                title_align="center"
            )
        except Exception:
            # Fallback confirmation dialog
            fallback_content = Text("Confirmation required", justify="center", style="white")
            return Panel(fallback_content, border_style="white", title="Confirm")