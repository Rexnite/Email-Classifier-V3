"""
emails_router.py

Exposes email endpoints:

    GET /emails/fetch
    GET /emails/export/csv
    GET /emails/export/md
    GET /emails/logs
    DELETE /emails/logs

These endpoints:
    1. Fetch unread Gmail messages
    2. Extract sender, subject, snippet and (for not-yet-cached messages)
       the full plain-text body
    3. Run local Ollama-powered urgency/importance/summary agents, skipping
       any message id already present in the local cache
    4. Return classified + summarized emails
    5. Export classified emails as CSV
    6. Export classified emails as Markdown digest
    7. Persist classification history to a local JSON log
"""

import base64
import csv
import io
from datetime import datetime

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from googleapiclient.errors import HttpError

from app.core.gmail_service import get_gmail_service, NotAuthenticatedError
from app.core.config import GMAIL_FETCH_QUERY, GMAIL_FETCH_MAX_RESULTS
from app.services.classifier_service import classify_gmail_emails
from app.services.cache_service import get_cached_emails
from app.services.digest_service import generate_markdown_digest
from app.services.log_service import (
    append_classification_logs,
    get_classification_logs,
    clear_classification_logs,
)
from agents.email_parser import parse_email

router = APIRouter(prefix="/emails", tags=["emails"])


def _parse_raw_message(raw_message: dict) -> dict:
    """
    Gmail's format="raw" returns the entire RFC 2822 message,
    base64url-encoded, in raw_message["raw"]. Decode it once and run it
    through the existing MIME parser to get sender/subject/date/body in
    a single pass.

    Returns a dict with sender/subject/date/body, all falling back to
    safe defaults if parsing fails for any reason -- this enrichment is
    on top of Gmail's own snippet, never load-bearing for the request.
    """
    raw_b64 = raw_message.get("raw", "")

    if not raw_b64:
        return {"sender": "(Unknown Sender)", "subject": "(No Subject)", "date": "", "body": ""}

    try:
        raw_bytes = base64.urlsafe_b64decode(raw_b64)
        parsed = parse_email(raw_bytes)
        return {
            "sender": parsed.get("sender") or "(Unknown Sender)",
            "subject": parsed.get("subject") or "(No Subject)",
            "date": parsed.get("date") or "",
            "body": parsed.get("body") or "",
        }
    except Exception:
        # Body/header extraction is an enrichment on top of the snippet --
        # never let a malformed/unusual message break the whole fetch.
        return {"sender": "(Unknown Sender)", "subject": "(No Subject)", "date": "", "body": ""}


def _fetch_unread_message_refs(service) -> list[dict]:
    try:
        list_response = (
            service.users()
            .messages()
            .list(
                userId="me",
                q=GMAIL_FETCH_QUERY,
                maxResults=GMAIL_FETCH_MAX_RESULTS,
            )
            .execute()
        )
    except HttpError as error:
        raise HTTPException(
            status_code=502,
            detail=f"Gmail API error while listing messages: {error}",
        )

    return list_response.get("messages", [])


def _fetch_and_classify_emails() -> list[dict]:
    try:
        service = get_gmail_service()
    except NotAuthenticatedError as error:
        raise HTTPException(status_code=401, detail=str(error))

    message_refs = _fetch_unread_message_refs(service)
    message_ids = [ref["id"] for ref in message_refs if ref.get("id")]

    # Only messages NOT already cached need a body fetch at all -- cached
    # messages will be skipped by classify_gmail_emails() below anyway, so
    # there is no point spending a (heavier) raw Gmail API call and a MIME
    # parse on them every single poll.
    cached_by_id = get_cached_emails(message_ids)

    emails = []

    for message_ref in message_refs:
        message_id = message_ref.get("id")

        if not message_id:
            continue

        if message_id in cached_by_id:
            # Already classified; classify_gmail_emails() will return the
            # cached entry untouched. No need to fetch anything from Gmail
            # for it beyond the id we already have.
            emails.append({"id": message_id})
            continue

        try:
            message = (
                service.users()
                .messages()
                .get(
                    userId="me",
                    id=message_id,
                    format="raw",
                )
                .execute()
            )
        except HttpError:
            continue

        # format="raw" does not return parsed headers/snippet the way
        # format="metadata" did -- sender/subject/date/body are all
        # extracted from the raw MIME message via email_parser. Gmail's
        # own "snippet" field is still returned alongside as a fallback.
        parsed = _parse_raw_message(message)

        emails.append(
            {
                "id": message.get("id", message_id),
                "sender": parsed["sender"],
                "subject": parsed["subject"],
                "date": parsed["date"],
                "snippet": message.get("snippet", ""),
                "body": parsed["body"],
            }
        )

    classified_emails = classify_gmail_emails(emails)
    append_classification_logs(classified_emails)

    return classified_emails


@router.get("/fetch")
def fetch_unread_emails():
    classified_emails = _fetch_and_classify_emails()

    return {
        "count": len(classified_emails),
        "emails": classified_emails,
    }


@router.get("/export/csv")
def export_classified_emails_csv():
    classified_emails = _fetch_and_classify_emails()

    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=[
            "id",
            "date",
            "sender",
            "subject",
            "snippet",
            "summary",
            "urgency",
            "importance",
            "classification",
            "classification_label",
            "classification_error",
        ],
    )

    writer.writeheader()

    for email in classified_emails:
        writer.writerow(
            {
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
        )

    output.seek(0)

    filename = f"email_classifier_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        },
    )


@router.get("/export/md")
def export_classified_emails_markdown():
    classified_emails = _fetch_and_classify_emails()

    markdown_digest = generate_markdown_digest(classified_emails)

    filename = f"email_classifier_digest_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

    return StreamingResponse(
        iter([markdown_digest]),
        media_type="text/markdown",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        },
    )


@router.get("/logs")
def get_email_classification_logs():
    logs = get_classification_logs()

    return {
        "count": len(logs),
        "logs": logs,
    }


@router.delete("/logs")
def clear_email_classification_logs():
    deleted_count = clear_classification_logs()

    return {
        "deleted": deleted_count,
        "message": "Email classification logs cleared successfully.",
    }