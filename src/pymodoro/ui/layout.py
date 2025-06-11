# src/pymodoro/ui/layout.py
from rich.table import Table
from rich.text import Text
from rich.align import Align
from typing import Any

class LayoutGrid:
    """Grid system for systematic component positioning."""
    
    @staticmethod
    def create_main_layout(min_width: int = 50) -> Table:
        """Create the main screen layout structure."""
        table = Table.grid(expand=True, padding=0)
        table.add_column(justify="center", no_wrap=True, min_width=min_width)
        return table
    
    @staticmethod
    def add_component(table: Table, component: Any) -> None:
        """Add a component to the layout grid."""
        table.add_row(component)
    
    @staticmethod
    def add_spacer(table: Table) -> None:
        """Add spacing between components."""
        table.add_row(Text(""))

class Alignment:
    """Helpers for centering and positioning content."""
    
    @staticmethod
    def center_vertical_and_horizontal(content: Any) -> Align:
        """Center content both vertically and horizontally."""
        return Align.center(content, vertical="middle")
    
    @staticmethod
    def center_horizontal(content: Any) -> Align:
        """Center content horizontally."""
        return Align.center(content)

class Spacing:
    """Utilities for consistent spacing and padding."""
    
    @staticmethod
    def create_help_text() -> Text:
        """Create the standard help text."""
        return Text("Press (h) for help", justify="center", style="dim")