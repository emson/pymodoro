# src/pymodoro/interface.py
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn
from rich.text import Text
from .timer import SessionType

console = Console()

def get_session_style(session_type: SessionType):
    if session_type == SessionType.WORK:
        return "bold white on red", "Work 🍅"
    elif session_type == SessionType.SHORT_BREAK:
        return "bold white on green", "Short Break ☕"
    return "bold white on blue", "Long Break 🛋️"


class PomodoroUI:
    def __init__(self, timer):
        self.timer = timer
        self.layout = self._create_layout()

    def _create_layout(self) -> Layout:
        layout = Layout(name="root")
        layout.split(
            Layout(name="header", size=3),
            Layout(ratio=1, name="main"),
            Layout(size=3, name="footer"),
        )
        layout["main"].split_row(Layout(name="side"), Layout(name="body", ratio=2))
        return layout

    def _create_header(self) -> Panel:
        title = Text("PyModoro - A Pomodoro Timer", justify="center", style="bold magenta")
        return Panel(title, border_style="magenta")

    def _create_footer(self) -> Panel:
        controls = Text(
            "SPACE: Pause/Resume | N: Skip Session | Q: Quit",
            justify="center",
            style="bold yellow",
        )
        return Panel(controls, border_style="yellow")

    def _create_status_panel(self) -> Panel:
        style, session_name = get_session_style(self.timer.current_session)
        
        status_text = Text(justify="center")
        status_text.append(f"{session_name}\n\n", style=style)
        status_text.append(f"Pomodoros Done: {self.timer.pomodoros_completed}\n")
        
        status = "Paused" if not self.timer.is_running else "Running"
        status_style = "yellow" if not self.timer.is_running else "cyan"
        status_text.append(f"Status: ", style="bold")
        status_text.append(f"{status}", style=status_style)

        return Panel(status_text, title="[bold]Status[/bold]", border_style="cyan")

    def _create_timer_panel(self) -> Panel:
        progress = Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=None, complete_style="bold white", finished_style="green"),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            expand=True
        )
        
        total_time = self.timer.settings[self.timer.current_session]
        remaining = max(0, self.timer.time_left)
        completed = total_time - remaining
        
        mins, secs = divmod(int(remaining), 60)
        time_str = f"{mins:02d}:{secs:02d}"
        
        style, session_name = get_session_style(self.timer.current_session)
        progress.add_task(f"[bold]{time_str}[/bold]", total=total_time, completed=completed)

        return Panel(progress, title=f"[bold]{session_name} Timer[/bold]", border_style=style.split(" on ")[1])

    def get_renderable(self) -> Layout:
        self.layout["header"].update(self._create_header())
        self.layout["footer"].update(self._create_footer())
        self.layout["side"].update(self._create_status_panel())
        self.layout["body"].update(self._create_timer_panel())
        return self.layout
