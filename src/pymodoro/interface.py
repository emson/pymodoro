# src/pymodoro/interface.py
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn
from rich.table import Table
from rich.text import Text
from .timer import SessionType

console = Console()

# The animation is removed. We now have a single, static piece of art.
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

class PomodoroUI:
    def __init__(self, timer):
        self.timer = timer

    def get_renderable(self, confirmation_type=None):
        """
        Builds the entire UI renderable from scratch on each update.
        This uses a borderless Table to vertically stack and center components.
        confirmation_type: None, 'skip', 'reset', 'quit', or 'help' to show overlay
        """
        # If showing confirmation or help, render the appropriate overlay
        if confirmation_type:
            if confirmation_type == 'help':
                return self._render_help()
            else:
                return self._render_confirmation(confirmation_type)
        
        # --- 1. Determine Session State and Colors ---
        is_work = self.timer.current_session == SessionType.WORK
        is_paused = not self.timer.is_running
        
        if is_work:
            primary_color = "red"
            status_icon = "🍅"
            status_text = f"{status_icon} Pomodoro #{self.timer.pomodoros_completed + 1}"
        else: # It's a break
            primary_color = "green" if self.timer.current_session == SessionType.SHORT_BREAK else "blue"
            status_icon = "☕" if self.timer.current_session == SessionType.SHORT_BREAK else "🛋️"
            status_text = f"{status_icon} Break"

        # Override colors and add text for paused state
        display_color = "yellow" if is_paused else primary_color
        if is_paused:
            status_text += " | [bold yellow]PAUSED[/bold yellow]"

        # --- 2. Create UI Components ---
        
        # Header text (e.g., "Work 🍅 | Pomodoro #1 | PAUSED")
        header = Text.from_markup(status_text, justify="center", style=f"bold {primary_color}")

        # The main timer display (e.g., "24:59") - yellow when paused
        mins, secs = divmod(int(self.timer.time_left), 60)
        time_display_str = f"{mins:02d}:{secs:02d}"
        timer_text = Text(time_display_str, justify="center", style="bold white on black")
        
        # Create a beautiful chunky progress bar using custom Text
        total_time = self.timer.settings[self.timer.current_session]
        remaining = max(0, self.timer.time_left)
        completed = total_time - remaining
        
        # Calculate progress percentage
        progress_ratio = completed / total_time if total_time > 0 else 0
        bar_width = 40
        filled_width = int(progress_ratio * bar_width)
        empty_width = bar_width - filled_width
        
        # Create chunky progress bar with block characters - yellow when paused
        filled_blocks = "█" * filled_width
        empty_blocks = "░" * empty_width
        
        # Create two identical rows for extra chunkiness
        progress_bar1 = Text(filled_blocks + empty_blocks, style=f"bold {display_color}")
        progress_bar2 = Text(filled_blocks + empty_blocks, style=f"bold {display_color}")
        
        # Stack the bars for thickness
        from rich.console import Group
        chunky_progress = Group(progress_bar1, progress_bar2)
        
        # Simple help message instead of cluttered controls
        help_text = Text("Press (h) for help", justify="center", style="dim")
        
        # --- 3. Assemble Components in a Table ---
        # A borderless table is used as a layout tool for vertical stacking.
        layout_table = Table.grid(expand=True)
        layout_table.add_row(header)
        layout_table.add_row("") # Whitespace

        # Show tomato art - yellow for paused, red for work, green for breaks
        if is_paused:
            layout_table.add_row(Align.center(Text.from_markup(PAUSE_TOMATO_ART)))
        elif is_work:
            layout_table.add_row(Align.center(Text.from_markup(TOMATO_ART)))
        else:
            layout_table.add_row(Align.center(Text.from_markup(BREAK_TOMATO_ART)))
        
        layout_table.add_row(Align.center(Panel(timer_text, width=12, style=display_color)))
        layout_table.add_row("") # Small spacing before progress bar
        layout_table.add_row(Align.center(chunky_progress))
        
        # Use a flexible amount of whitespace to push help text to the bottom
        layout_table.add_row("")
        layout_table.add_row("")
        layout_table.add_row(help_text)

        # The final renderable is aligned in the center of the screen
        return Align.center(layout_table, vertical="middle")

    def _render_help(self):
        """
        Renders a clean help screen with keyboard shortcuts
        """
        # Determine colors based on current session
        is_work = self.timer.current_session == SessionType.WORK
        is_paused = not self.timer.is_running
        
        if is_work:
            border_color = "red"
        else:
            border_color = "green" if self.timer.current_session == SessionType.SHORT_BREAK else "blue"
        
        # Override with yellow if paused
        if is_paused:
            border_color = "yellow"
        
        # Create help table with keyboard shortcuts
        help_table = Table(show_header=False, box=None, padding=(0, 2))
        help_table.add_column("Key", style="bold cyan", width=8)
        help_table.add_column("Action", style="white")
        
        # Add keyboard shortcuts
        help_table.add_row("SPACE", "Pause/Resume the current session")
        help_table.add_row("n", "Skip to next session (with confirmation)")
        help_table.add_row("r", "Reset current session (with confirmation)")
        help_table.add_row("q", "Quit application (with confirmation)")
        help_table.add_row("h", "Show/hide this help screen")
        help_table.add_row("", "")  # Empty row for spacing
        help_table.add_row("ESC", "Close this help screen")
        
        # Show current session context
        mins, secs = divmod(int(self.timer.time_left), 60)
        time_str = f"{mins:02d}:{secs:02d}"
        
        if is_work:
            session_text = f"Work Session - {time_str} remaining"
            status_text = f"Pomodoro #{self.timer.pomodoros_completed + 1}"
        else:
            session_name = "Short Break" if self.timer.current_session == SessionType.SHORT_BREAK else "Long Break"
            session_text = f"{session_name} - {time_str} remaining"
            status_text = "Break Time"
        
        if is_paused:
            session_text += " (PAUSED)"
        
        context_text = Text(f"Current: {session_text}", style="dim", justify="center")
        status_display = Text(status_text, style=f"bold {border_color}", justify="center")
        
        from rich.console import Group
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
        
        # Create help panel
        help_panel = Panel(
            help_content,
            border_style=f"bold {border_color}",
            padding=(2, 4),
            width=65,
            title="[bold]🍅 Pymodoro Help[/bold]",
            title_align="center"
        )
        
        # Center the help screen
        return Align.center(help_panel, vertical="middle")

    def _render_confirmation(self, confirmation_type):
        """
        Renders a full-screen confirmation dialog
        """
        # Determine colors based on current session
        is_work = self.timer.current_session == SessionType.WORK
        is_paused = not self.timer.is_running
        
        if is_work:
            border_color = "red"
        else:
            border_color = "green" if self.timer.current_session == SessionType.SHORT_BREAK else "blue"
        
        # Override with yellow if paused
        if is_paused:
            border_color = "yellow"
        
        # Create confirmation content based on type
        if confirmation_type == 'skip':
            if is_work:
                title = "Skip Work Session?"
                message = f"Skip current work session and start break?\nYou'll lose progress on Pomodoro #{self.timer.pomodoros_completed + 1}."
            else:
                title = "Skip Break?"
                message = "Skip current break and start next work session?"
        elif confirmation_type == 'reset':
            if is_work:
                title = "Reset Work Session?"
                message = f"Reset current work session to full duration?\nPomodoro #{self.timer.pomodoros_completed + 1} will restart from the beginning."
            else:
                session_name = "Short Break" if self.timer.current_session == SessionType.SHORT_BREAK else "Long Break"
                title = f"Reset {session_name}?"
                message = f"Reset current {session_name.lower()} to full duration?\nThe break will restart from the beginning."
        else:  # quit
            title = "Quit Pymodoro?"
            message = "Are you sure you want to quit?\nAll progress will be lost."
        
        # Show current timer context
        mins, secs = divmod(int(self.timer.time_left), 60)
        time_str = f"{mins:02d}:{secs:02d}"
        
        if is_work:
            context = f"Current: Work Session - {time_str} remaining"
        else:
            session_name = "Short Break" if self.timer.current_session == SessionType.SHORT_BREAK else "Long Break"
            context = f"Current: {session_name} - {time_str} remaining"
        
        # Create the confirmation dialog content
        title_text = Text(title, style=f"bold {border_color}", justify="center")
        context_text = Text(context, style="dim", justify="center")
        message_text = Text(message, style="white", justify="center")
        options_text = Text("Y - Yes    N - No    SPACE - Cancel", style="bold white", justify="center")
        
        from rich.console import Group
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
        
        # Create a beautiful modal panel
        modal_panel = Panel(
            confirmation_content,
            border_style=f"bold {border_color}",
            padding=(2, 4),
            width=60,
            title="[bold]Confirmation Required[/bold]",
            title_align="center"
        )
        
        # Center the modal on screen
        return Align.center(modal_panel, vertical="middle")