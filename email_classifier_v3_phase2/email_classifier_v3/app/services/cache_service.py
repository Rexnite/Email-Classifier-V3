"""
cache_service.py

Persistent local cache of classified (and now summarized) emails, keyed
by Gmail message id.

Why this exists:
The frontend polls /emails/fetch every 30 seconds. Without a cache, every
poll re-runs the full Ollama pipeline (urgency + importance + summary)
for every email returned by Gmail's search query, even if that email was
already processed seconds ago. This file lets the rest of the backend
skip Ollama entirely for any message id it has already classified.

Stored in:
    cache/email_classification_cache.json

This is intentionally separate from logs/ (an append-only history) and
from token.json/credentials.json (must never live here).
"""

import json
from pathlib import Path
from threading import Lock
from typing import Optional

CACHE_DIR = Path("cache")
CACHE_FILE = CACHE_DIR / "email_classification_cache.json"

_cache_lock = Lock()


def _ensure_cache_file_exists():
    CACHE_DIR.mkdir(exist_ok=True)

    if not CACHE_FILE.exists():
        CACHE_FILE.write_text("{}", encoding="utf-8")


def _read_cache() -> dict:
    _ensure_cache_file_exists()

    try:
        with CACHE_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, dict):
            return data

        return {}

    except json.JSONDecodeError:
        return {}


def _write_cache(cache: dict):
    _ensure_cache_file_exists()

    with CACHE_FILE.open("w", encoding="utf-8") as file:
        json.dump(cache, file, indent=2, ensure_ascii=False)


def get_cached_email(email_id: str) -> Optional[dict]:
    """
    Returns the previously cached, fully-classified email dict for this
    Gmail message id, or None if it has not been processed yet.
    """
    if not email_id:
        return None

    with _cache_lock:
        cache = _read_cache()
        return cache.get(email_id)


def get_cached_emails(email_ids: list[str]) -> dict:
    """
    Bulk lookup. Returns {id: cached_entry} for whichever of the given
    ids are already cached. Ids not present in the cache are simply
    omitted from the result.
    """
    if not email_ids:
        return {}

    with _cache_lock:
        cache = _read_cache()
        return {
            email_id: cache[email_id]
            for email_id in email_ids
            if email_id in cache
        }


def store_classified_email(classified_email: dict) -> None:
    """
    Saves (or overwrites) the cache entry for one classified email,
    keyed by its Gmail message id. Emails with classification_error set
    are still cached -- re-running a failing classification on every poll
    would defeat the point of caching and just keeps hammering Ollama for
    a message that is failing for some other reason.
    """
    email_id = classified_email.get("id")

    if not email_id:
        return

    with _cache_lock:
        cache = _read_cache()
        cache[email_id] = classified_email
        _write_cache(cache)


def store_classified_emails(classified_emails: list[dict]) -> None:
    if not classified_emails:
        return

    with _cache_lock:
        cache = _read_cache()

        for email in classified_emails:
            email_id = email.get("id")
            if email_id:
                cache[email_id] = email

        _write_cache(cache)


def clear_cache() -> int:
    with _cache_lock:
        cache = _read_cache()
        count = len(cache)
        _write_cache({})
        return count
