# src/pymodoro/session_model.py

from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class Session(BaseModel):
    """Represents a single Pomodoro work session."""
    start: datetime
    duration_minutes: int = Field(25, gt=0)
    notes: Optional[str] = None


class DayLog(BaseModel):
    """Represents the log for a single day, containing all sessions."""
    log_date: date
    sessions: List[Session] = Field(default_factory=list)

    @property
    def session_count(self) -> int:
        """Returns the number of completed sessions for the day."""
        return len(self.sessions)