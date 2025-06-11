# Feature: Persistent Daily Session Logging

## 📜 Overview & Goal

The primary goal of this feature is to make the Pymodoro timer stateful by persisting session data. Each completed Pomodoro session will be saved to a daily log file in YAML format. This allows for session history, tracking productivity over time, and resuming session counts across application restarts.

The design emphasizes data integrity, cross-platform compatibility, and human-readability of the log files.

## 🎯 Key Priorities

1.  **Data Integrity**: Session data is valuable. We must prevent data loss, even if the application crashes during a write operation. Atomic writes are non-negotiable.
2.  **Robustness**: The application must gracefully handle scenarios like missing log files, corrupted data, and file permission issues.
3.  **Cross-Platform Compatibility**: The feature must work seamlessly on Linux, macOS, and Windows. File paths will be resolved using the XDG Base Directory Specification.
4.  **Simplicity & Maintainability**: The implementation should be straightforward, leveraging Pydantic for data validation and standard libraries for file operations to ensure the code is easy to understand and maintain.

## 📂 File Storage and Management

Session logs will be stored in a dedicated, platform-appropriate directory.

-   **Path Strategy**: We will adhere to the XDG Base Directory Specification.
    -   The base directory will be resolved from the `$XDG_STATE_HOME` environment variable.
    -   **Fallback on UNIX/macOS**: `~/.local/state`
    -   **Fallback on Windows**: `%APPDATA%` (e.g., `C:\Users\<user>\AppData\Roaming`)
-   **Directory Structure**: Logs will be stored under `<base_directory>/pymodoro/logs/`.
-   **File Naming**: Each log file will be named after the date of the session in `YYYY-MM-DD.yaml` format.
-   **Automation**: The application must automatically create the necessary directories on its first run.

## 📝 Data Schema

We will use Pydantic to define a strict schema for our session data, which ensures type safety and validation at runtime. The data will be serialized to a human-readable YAML format.

### Pydantic Models

```python
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
    sessions: List[Session] = []

    @property
    def session_count(self) -> int:
        """Returns the number of completed sessions for the day."""
        return len(self.sessions)
```

### Example YAML File (`2024-08-07.yaml`)

```yaml
log_date: 2024-08-07
sessions:
  - start: '2024-08-07T09:05:15.123456'
    duration_minutes: 25
    notes: 'Drafted initial feature specification.'
  - start: '2024-08-07T09:35:45.567890'
    duration_minutes: 25
    notes: 'Implemented Pydantic models and file path logic.'
```

## 🔄 Core Workflow

### A. Application Start-Up

1.  Determine the path for today's log file (e.g., `.../pymodoro/logs/2024-08-07.yaml`).
2.  If the file exists, load and parse it using `yaml.safe_load()`.
3.  Validate the loaded data against the `DayLog` Pydantic model.
4.  If the file does not exist or is empty, initialize a new `DayLog` object for the current date.
5.  The `DayLog.session_count` property will provide the session count for the day so far.

### B. Session Completion

1.  When a Pomodoro timer finishes a session, record the `start` datetime and `duration`.
2.  (Optional) Prompt the user to enter brief notes for the session (manually in the YAML file)
3.  Create a new `Session` object with this data.
4.  Append the new `Session` to the `sessions` list of the current `DayLog` object.
5.  Save the entire `DayLog` object back to the YAML file using an atomic write operation to prevent data corruption.

## ⚠️ Edge Cases and Recovery

-   **Corrupt YAML File**: If `yaml.safe_load()` fails or Pydantic validation throws an error, the corrupt file should be backed up (e.g., renamed to `YYYY-MM-DD.yaml.corrupt`) and a new, empty log for the day should be created. A warning should be logged.
-   **Atomic Write Failure**: The atomic write process involves writing to a temporary file (`.tmp`) and then renaming it. If the app crashes, a `.tmp` file might be left behind. On startup, if a `.tmp` file exists, it can be considered more recent and used to recover data, but the primary log file should not be overwritten without a clear recovery strategy. For simplicity, we can start by just logging a warning if a stale `.tmp` file is found.
-   **Cross-Midnight Sessions**: A session will be logged to the date on which it *started*. This is the simplest approach and avoids complexity.
-   **Permissions**: The application should handle `PermissionError` when creating directories or writing files and log a clear error message to the user.

## ✅ Implementation Tasks

- [x] **1. Setup & Dependencies**:
    - [x] Create a new directory `docs_ai`.
    - [x] Create this file `docs_ai/feature_save_session.md`.
    - [x] Add `PyYAML` and `pydantic` to the project dependencies.

- [x] **2. Data Models**:
    - [x] Create a new file `src/pymodoro/session_model.py`.
    - [x] Implement the `Session` and `DayLog` Pydantic models as defined in the schema section.

- [x] **3. Storage Utility**:
    - [x] Create a new file `src/pymodoro/storage.py`.
    - [x] Implement a function `get_log_file_path() -> Path` that resolves the correct path for the current day's log file according to the XDG specification. This function should also ensure the containing directories exist, creating them if necessary (`mkdir(parents=True, exist_ok=True)`).

- [x] **4. Core Logic**:
    - [x] In `src/pymodoro/storage.py`, implement `load_or_initialize_day_log() -> DayLog`. This function will use `get_log_file_path()` and handle loading, validation, and initialization of a new log if one doesn't exist or is corrupt.
    - [x] In `src/pymodoro/storage.py`, implement `save_day_log(day_log: DayLog)`. This function must perform an atomic write to the log file.

- [x] **5. Application Integration**:
    - [x] In the main application logic, call `load_or_initialize_day_log()` on startup to load the session data.
    - [x] Update the UI/display to reflect the session count from the loaded `DayLog` object.
    - [x] When a session completes, create and append a new `Session` object to the `DayLog`.
    - [x] Call `save_day_log()` to persist the updated `DayLog`.

- [ ] **6. User Interaction**:
    - [ ] After a session completes, add a simple mechanism to prompt the user for notes. An empty note is acceptable.

- [ ] **7. Testing**:
    - [ ] Write unit tests for `get_log_file_path()` to verify correct path resolution on different platforms (can be mocked).
    - [ ] Write tests for `load_or_initialize_day_log` and `save_day_log` to cover success, file-not-found, and corruption scenarios. 