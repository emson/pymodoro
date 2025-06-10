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

class PomodoroUI:
    def __init__(self, timer):
        self.timer = timer

    def get_renderable(self):
        """
        Builds the entire UI renderable from scratch on each update.
        This uses a borderless Table to vertically stack and center components.
        """
        # --- 1. Determine Session State and Colors ---
        is_work = self.timer.current_session == SessionType.WORK
        
        if is_work:
            primary_color = "red"
            status_icon = "🍅"
            status_text = f"Work {status_icon} | Pomodoro #{self.timer.pomodoros_completed + 1}"
        else: # It's a break
            primary_color = "green" if self.timer.current_session == SessionType.SHORT_BREAK else "blue"
            status_icon = "☕" if self.timer.current_session == SessionType.SHORT_BREAK else "🛋️"
            status_text = f"Break {status_icon}"

        # --- 2. Create UI Components ---
        
        # Header text (e.g., "Work 🍅 | Pomodoro #1")
        header = Text(status_text, justify="center", style=f"bold {primary_color}")

        # The main timer display (e.g., "24:59")
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
        
        # Create chunky progress bar with block characters
        filled_blocks = "█" * filled_width
        empty_blocks = "░" * empty_width
        
        # Create two identical rows for extra chunkiness
        progress_bar1 = Text(filled_blocks + empty_blocks, style=f"bold {primary_color}")
        progress_bar2 = Text(filled_blocks + empty_blocks, style=f"bold {primary_color}")
        
        # Stack the bars for thickness
        from rich.console import Group
        chunky_progress = Group(progress_bar1, progress_bar2)
        
        # Footer controls text
        controls = Text("SPACE: Pause/Resume | N: Skip | Q: Quit", justify="center", style="dim")
        
        # --- 3. Assemble Components in a Table ---
        # A borderless table is used as a layout tool for vertical stacking.
        layout_table = Table.grid(expand=True)
        layout_table.add_row(header)
        layout_table.add_row("") # Whitespace

        # Only show the tomato during work sessions
        if is_work:
            layout_table.add_row(Align.center(Text.from_markup(TOMATO_ART)))
        
        layout_table.add_row(Align.center(Panel(timer_text, width=12, style=primary_color)))
        layout_table.add_row("") # Small spacing before progress bar
        layout_table.add_row(Align.center(chunky_progress))
        
        # Use a flexible amount of whitespace to push controls to the bottom
        layout_table.add_row("")
        layout_table.add_row(controls)

        # The final renderable is aligned in the center of the screen
        return Align.center(layout_table, vertical="middle")