"""
classifier_service.py

Connects Gmail-fetched emails to the local Ollama-powered agentic
classification pipeline.

Pipeline:
    Gmail email
        -> Urgency Agent
        -> Importance Agent
        -> Coordinator
        -> Eisenhower Matrix category
        -> Summary Agent (additional, independent layer)

Caching:
    classify_gmail_emails() is cache-aware: any email whose Gmail message
    id is already present in the local cache (app/services/cache_service)
    is returned as-is, with no Ollama calls made for it at all. Only
    emails not yet seen are run through the pipeline below and then
    written to the cache.
"""

from agents.urgency_agent import evaluate_urgency
from agents.importance_agent import evaluate_importance
from agents.coordinator import classify_email, CATEGORY_LABELS
from agents.summary_agent import summarize_email
from app.services.cache_service import get_cached_emails, store_classified_emails


OLLAMA_MODEL = "qwen2.5:3b"


def classify_gmail_email(email_data: dict) -> dict:
    """
    Takes one Gmail email object and returns the same object enriched with:
        urgency
        importance
        classification
        classification_label
        summary

    Does not consult or write to the cache -- this function always runs
    the full pipeline. Use classify_gmail_emails() for cache-aware
    behavior across a batch of emails.
    """

    sender = email_data.get("sender", "")
    subject = email_data.get("subject", "")
    snippet = email_data.get("snippet", "")

    # Prefer the full extracted body (added by emails_router's MIME
    # parsing) when present; fall back to Gmail's short snippet for any
    # email where full-body extraction failed or wasn't available. This
    # only improves the input text the agents already use -- the
    # urgency/importance prompts and logic are unchanged.
    body = email_data.get("body") or snippet or ""

    try:
        urgency = evaluate_urgency(
            subject=subject,
            body=body,
            model=OLLAMA_MODEL,
        )

        importance = evaluate_importance(
            subject=subject,
            body=body,
            sender=sender,
            model=OLLAMA_MODEL,
        )

        classification = classify_email(
            urgent=urgency,
            important=importance,
        )

        try:
            summary = summarize_email(
                subject=subject,
                body=body,
                model=OLLAMA_MODEL,
            )
            summary_error = None
        except Exception as summary_error_obj:
            # Summarization failing should never take down urgency/importance
            # classification, which is the core feature. Surface the failure
            # on its own field instead.
            summary = None
            summary_error = str(summary_error_obj)

        return {
            **email_data,
            "urgency": urgency,
            "importance": importance,
            "classification": classification,
            "classification_label": CATEGORY_LABELS.get(classification, "Unknown"),
            "classification_error": None,
            "summary": summary,
            "summary_error": summary_error,
        }

    except Exception as error:
        return {
            **email_data,
            "urgency": "PENDING",
            "importance": "PENDING",
            "classification": "unclassified",
            "classification_label": "Unclassified",
            "classification_error": str(error),
            "summary": None,
            "summary_error": None,
        }


def classify_gmail_emails(emails: list[dict]) -> list[dict]:
    """
    Classifies a list of Gmail emails, skipping Ollama entirely for any
    email whose message id is already cached.

    Order of the input list is preserved in the output.
    """
    if not emails:
        return []

    email_ids = [email.get("id") for email in emails if email.get("id")]
    cached_by_id = get_cached_emails(email_ids)

    results = []
    newly_classified = []

    for email in emails:
        email_id = email.get("id")
        cached_entry = cached_by_id.get(email_id) if email_id else None

        if cached_entry is not None:
            results.append(cached_entry)
            continue

        classified = classify_gmail_email(email)
        results.append(classified)
        newly_classified.append(classified)

    if newly_classified:
        store_classified_emails(newly_classified)

    return results