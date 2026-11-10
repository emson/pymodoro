"""A corrupt day-log file must not kill the CLI on startup.

`load_or_initialize_day_log` promises to back a corrupt file up and start
fresh, but a YAML document that is not a mapping (a scalar, a list, ...)
reached `DayLog(**data)` as a `TypeError`, which was not handled, so the
whole application died instead of recovering.
"""

from datetime import date, datetime

import pymodoro.storage as storage_mod
from pymodoro.storage import (
    load_or_initialize_day_log,
    save_day_log,
)


def _patch_log_path(monkeypatch, tmp_path):
    log = tmp_path / "2026-11-10.yaml"
    monkeypatch.setattr(storage_mod, "get_log_file_path", lambda: log)
    return log


def test_scalar_yaml_log_starts_fresh(tmp_path, monkeypatch):
    log = _patch_log_path(monkeypatch, tmp_path)
    log.write_text("just a scalar string, not a mapping", encoding="utf-8")

    day_log = load_or_initialize_day_log()

    assert day_log.sessions == []
    assert day_log.log_date == date.today()
    assert log.with_suffix(".yaml.corrupt").exists()


def test_list_yaml_log_starts_fresh(tmp_path, monkeypatch):
    log = _patch_log_path(monkeypatch, tmp_path)
    log.write_text("- session one\n- session two\n", encoding="utf-8")

    day_log = load_or_initialize_day_log()

    assert day_log.sessions == []
    assert log.with_suffix(".yaml.corrupt").exists()


def test_valid_log_still_loads(tmp_path, monkeypatch):
    from pymodoro.session_model import DayLog, Session

    _patch_log_path(monkeypatch, tmp_path)
    save_day_log(
        DayLog(
            log_date=date.today(),
            sessions=[Session(start=datetime(2026, 11, 10, 12, 0, 0))],
        )
    )

    day_log = load_or_initialize_day_log()

    assert len(day_log.sessions) == 1
    assert day_log.sessions[0].start == datetime(2026, 11, 10, 12, 0, 0)
