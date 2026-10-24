"""
digest_service.py

Generates Markdown digests from classified Gmail emails.

The digest groups emails by Eisenhower Matrix category:

    1. Urgent + Important
    2. Important, Not Urgent
    3. Urgent, Not Important
    4. Neither
    5. Unclassified / Errors
"""

from datetime import datetime


CATEGORY_ORDER = [
    "urgent-important",
    "important-not-urgent",
    "urgent-not-important",
    "neither",
    "unclassified",
]


CATEGORY_TITLES = {
    "urgent-important": "Urgent + Important",
    "important-not-urgent": "Important, Not Urgent",
    "urgent-not-important": "Urgent, Not Important",
    "neither": "Neither",
    "unclassified": "Unclassified / Errors",
}


def _safe_text(value) -> str:
    if value is None:
        return ""

    text = str(value)
    return text.replace("\r", " ").replace("\n", " ").strip()


def _group_emails_by_category(emails: list[dict]) -> dict[str, list[dict]]:
    grouped = {category: [] for category in CATEGORY_ORDER}

    for email in emails:
        category = email.get("classification") or "unclassified"

        if category not in grouped:
            category = "unclassified"

        grouped[category].append(email)

    return grouped


def generate_markdown_digest(emails: list[dict]) -> str:
    grouped = _group_emails_by_category(emails)

    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = [
        "# Email Classifier V3 Digest",
        "",
        f"**Generated At:** {generated_at}",
        f"**Total Emails:** {len(emails)}",
        "",
        "---",
        "",
        "## Summary",
        "",
        "| Category | Count |",
        "|---|---:|",
    ]

    for category in CATEGORY_ORDER:
        title = CATEGORY_TITLES[category]
        count = len(grouped[category])
        lines.append(f"| {title} | {count} |")

    lines.extend(["", "---", ""])

    for category in CATEGORY_ORDER:
        title = CATEGORY_TITLES[category]
        category_emails = grouped[category]

        lines.append(f"## {title}")
        lines.append("")

        if not category_emails:
            lines.append("_No emails in this category._")
            lines.append("")
            continue

        for index, email in enumerate(category_emails, start=1):
            sender = _safe_text(email.get("sender", "(Unknown Sender)"))
            subject = _safe_text(email.get("subject", "(No Subject)"))
            date = _safe_text(email.get("date", ""))
            snippet = _safe_text(email.get("snippet", ""))
            summary = _safe_text(email.get("summary", ""))
            urgency = _safe_text(email.get("urgency", ""))
            importance = _safe_text(email.get("importance", ""))
            classification_label = _safe_text(
                email.get("classification_label", title)
            )
            classification_error = _safe_text(
                email.get("classification_error", "")
            )

            lines.append(f"### {index}. {subject}")
            lines.append("")
            lines.append(f"- **Sender:** {sender}")

            if date:
                lines.append(f"- **Date:** {date}")

            lines.append(f"- **Urgency:** {urgency}")
            lines.append(f"- **Importance:** {importance}")
            lines.append(f"- **Category:** {classification_label}")

            if classification_error:
                lines.append(f"- **Classification Error:** {classification_error}")

            if summary:
                lines.append("")
                lines.append("**Summary:**")
                lines.append("")
                lines.append(summary)

            if snippet:
                lines.append("")
                lines.append("**Preview:**")
                lines.append("")
                lines.append(f"> {snippet}")

            lines.append("")
            lines.append("---")
            lines.append("")

    return "\n".join(lines)