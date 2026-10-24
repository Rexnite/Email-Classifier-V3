import re
import email
from email.header import decode_header
from bs4 import BeautifulSoup


def decode_mime_text(value):
    if not value:
        return ""

    decoded_parts = decode_header(value)
    result = ""

    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            try:
                result += part.decode(encoding or "utf-8", errors="ignore")
            except Exception:
                result += part.decode("utf-8", errors="ignore")
        else:
            result += part

    return result.strip()


def clean_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator="\n")
    return clean_text(text)


def clean_text(text):
    if not text:
        return ""

    text = text.replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)

    junk_patterns = [
        r"click here to unsubscribe.*",
        r"unsubscribe.*",
        r"view this email in your browser.*",
        r"this email was sent to.*",
        r"confidentiality notice.*",
    ]

    for pattern in junk_patterns:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE | re.DOTALL)

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines).strip()


def extract_body(message):
    plain_text = ""
    html_text = ""

    if message.is_multipart():
        for part in message.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition") or "").lower()

            if "attachment" in content_disposition:
                continue

            payload = part.get_payload(decode=True)
            if not payload:
                continue

            charset = part.get_content_charset() or "utf-8"

            try:
                content = payload.decode(charset, errors="ignore")
            except Exception:
                content = payload.decode("utf-8", errors="ignore")

            if content_type == "text/plain":
                plain_text += clean_text(content) + "\n"
            elif content_type == "text/html":
                html_text += clean_html(content) + "\n"

    else:
        payload = message.get_payload(decode=True)

        if payload:
            charset = message.get_content_charset() or "utf-8"

            try:
                content = payload.decode(charset, errors="ignore")
            except Exception:
                content = payload.decode("utf-8", errors="ignore")

            if message.get_content_type() == "text/html":
                html_text = clean_html(content)
            else:
                plain_text = clean_text(content)

    return plain_text.strip() or html_text.strip() or "(No body found)"


def parse_email(raw_email_bytes):
    message = email.message_from_bytes(raw_email_bytes)

    sender = decode_mime_text(message.get("From"))
    subject = decode_mime_text(message.get("Subject"))
    date = decode_mime_text(message.get("Date"))
    body = extract_body(message)

    return {
        "sender": sender or "(Unknown Sender)",
        "subject": subject or "(No Subject)",
        "date": date or "(No Date)",
        "body": body,
    }