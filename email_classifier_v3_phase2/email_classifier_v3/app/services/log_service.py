"""
log_service.py

Persistent local logging for Email Classifier V3.

Stores classified email results in:

    logs/email_classification_log.json

This is intentionally separate from OAuth token files.
Do not store token.json or credentials.json here.
"""

import json
from datetime import datetime
from pathlib import Path
from threading import Lock


LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "email_classification_log.json"

_log_lock = Lock()


def _ensure_log_file_exists():
    LOG_DIR.mkdir(exist_ok=True)

    if not LOG_FILE.exists():
        LOG_FILE.write_text("[]", encoding="utf-8")


def _read_existing_logs() -> list[dict]:
    _ensure_log_file_exists()

    try:
        with LOG_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data

        return []

    except json.JSONDecodeError:
        return []


def _write_logs(logs: list[dict]):
    _ensure_log_file_exists()

    with LOG_FILE.open("w", encoding="utf-8") as file:
        json.dump(logs, file, indent=2, ensure_ascii=False)


def build_log_entry(email: dict) -> dict:
    return {
        "logged_at": datetime.now().isoformat(timespec="seconds"),
        "id": email.get("id", ""),
        "date": email.get("date", ""),
        "sender": email.get("sender", ""),
        "subject": email.get("subject", ""),
        "snippet": email.get("snippet", ""),
        "summary": email.get("summary", ""),
        "urgency": email.get("urgency", ""),
        "importance": email.get("importance", ""),
        "classification": email.get("classification", ""),
        "classification_label": email.get("classification_label", ""),
        "classification_error": email.get("classification_error", ""),
    }


def append_classification_logs(emails: list[dict]) -> int:
    """
    Appends classification results to the JSON log.

    Uses Gmail message id to avoid duplicating the same email repeatedly
    during frontend polling.
    """

    if not emails:
        return 0

    with _log_lock:
        existing_logs = _read_existing_logs()
        existing_ids = {
            entry.get("id")
            for entry in existing_logs
            if entry.get("id")
        }

        new_entries = []

        for email in emails:
            email_id = email.get("id")

            if email_id and email_id in existing_ids:
                continue

            new_entries.append(build_log_entry(email))

        if not new_entries:
            return 0

        existing_logs.extend(new_entries)
        _write_logs(existing_logs)

        return len(new_entries)


def get_classification_logs() -> list[dict]:
    with _log_lock:
        return _read_existing_logs()


def clear_classification_logs() -> int:
    with _log_lock:
        existing_logs = _read_existing_logs()
        count = len(existing_logs)
        _write_logs([])
        return count