# src/pymodoro/storage.py

import os
import platform
import tempfile
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Optional

import yaml
from pydantic import ValidationError

from pymodoro.session_model import DayLog, Session


def get_log_file_path() -> Path:
    """Get the path for today's log file according to XDG spec."""
    system = platform.system()
    
    if system == "Windows":
        base_dir = Path(os.environ.get("APPDATA", "~")).expanduser()
    else:
        # Unix/Linux/macOS
        base_dir = Path(os.environ.get("XDG_STATE_HOME", "~/.local/state")).expanduser()
    
    log_dir = base_dir / "pymodoro" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    today = date.today()
    return log_dir / f"{today.isoformat()}.yaml"


def load_or_initialize_day_log() -> DayLog:
    """Load today's log file or initialize a new one."""
    log_file = get_log_file_path()
    today = date.today()
    
    if not log_file.exists():
        return DayLog(log_date=today)
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}
        
        return DayLog(**data)
    
    except (yaml.YAMLError, ValidationError, OSError) as e:
        # Back up corrupt file and start fresh
        backup_path = log_file.with_suffix('.yaml.corrupt')
        try:
            log_file.rename(backup_path)
        except OSError:
            pass
        
        return DayLog(log_date=today)


def save_day_log(day_log: DayLog) -> None:
    """Save the day log using atomic write."""
    log_file = get_log_file_path()
    
    # Prepare data for YAML serialization
    data = day_log.model_dump(mode='python')
    
    # Convert datetime objects to human-readable ISO format strings
    for session in data['sessions']:
        if 'start' in session:
            # Format as YYYY-MM-DD HH:MM:SS for human readability while maintaining ISO compliance
            session['start'] = session['start'].strftime('%Y-%m-%d %H:%M:%S')
    
    # Atomic write using temporary file
    with tempfile.NamedTemporaryFile(
        mode='w',
        encoding='utf-8',
        dir=log_file.parent,
        delete=False,
        suffix='.tmp'
    ) as tmp_file:
        yaml.safe_dump(data, tmp_file, default_flow_style=False)
        tmp_path = Path(tmp_file.name)
    
    try:
        tmp_path.replace(log_file)
    except OSError:
        tmp_path.unlink(missing_ok=True)
        raise


def add_session(duration_minutes: int = 25, notes: Optional[str] = None) -> None:
    """Add a new session to today's log."""
    from datetime import datetime
    
    day_log = load_or_initialize_day_log()
    session = Session(
        start=datetime.now(),
        duration_minutes=duration_minutes,
        notes=notes
    )
    day_log.sessions.append(session)
    save_day_log(day_log)


def reset_today_log() -> None:
    """Reset today's log to empty."""
    from datetime import date
    
    day_log = DayLog(log_date=date.today())
    save_day_log(day_log)


def open_log_in_editor() -> None:
    """Open today's log file in the system's default editor."""
    log_file = get_log_file_path()
    
    # Ensure log file exists
    if not log_file.exists():
        day_log = load_or_initialize_day_log()
        save_day_log(day_log)
    
    # Use Unix editor precedence: $VISUAL -> $EDITOR -> vim
    system = platform.system()
    try:
        if system == "Windows":
            subprocess.run(["start", str(log_file)], shell=True, check=True)
        else:  # macOS, Linux, Unix
            # Follow Unix convention: VISUAL > EDITOR > vim
            editor = (os.environ.get("VISUAL") or 
                     os.environ.get("EDITOR") or 
                     "vim")
            subprocess.run([editor, str(log_file)], check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Fallback: print file path for manual opening
        print(f"Could not open editor. Log file location: {log_file}")
        sys.exit(1)