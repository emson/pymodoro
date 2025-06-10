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
        confirmation_type: None, 'skip', or 'quit' to show confirmation dialog
        """
        # If showing confirmation, render the confirmation dialog
        if confirmation_type:
            return self._render_confirmation(confirmation_type)
        
        # --- 1. Determine Session State and Colors ---
        is_work = self.timer.current_session == SessionType.WORK
        is_paused = not self.timer.is_running
        
        if is_work:
            primary_color = "red"
            status_icon = "🍅"
            status_text = f"Work {status_icon} | Pomodoro #{self.timer.pomodoros_completed + 1}"
        else: # It's a break
            primary_color = "green" if self.timer.current_session == SessionType.SHORT_BREAK else "blue"
            status_icon = "☕" if self.timer.current_session == SessionType.SHORT_BREAK else "🛋️"
            status_text = f"Break {status_icon}"

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
        
        # Footer controls text
        controls = Text("(space) pause | (n)ext | (q)uit", justify="center", style="dim")
        
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
        
        # Use a flexible amount of whitespace to push controls to the bottom
        layout_table.add_row("")
        layout_table.add_row("")
        layout_table.add_row(controls)

        # The final renderable is aligned in the center of the screen
        return Align.center(layout_table, vertical="middle")

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