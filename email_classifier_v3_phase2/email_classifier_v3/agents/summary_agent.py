"""
summary_agent.py

Generates a short (2-4 sentence) summary of an email using the local
Ollama model. This is an additive layer on top of the existing
urgency/importance/coordinator pipeline -- it does not influence and is
not influenced by classification.
"""

from agents.ollama_client import ask_ollama

# Local 3B models lose coherence and slow down a lot on very long inputs.
# Truncating keeps latency predictable without materially hurting summary
# quality, since the first ~6000 characters of an email almost always
# contain the substantive content (signatures/footers/disclaimers/quoted
# threads trail off after that).
MAX_BODY_CHARS_FOR_SUMMARY = 6000

# Summaries are short prose, not a single token like YES/NO, so they need
# materially more headroom than the urgency/importance agents.
SUMMARY_NUM_PREDICT = 160


def _truncate_body(body: str) -> str:
    if not body:
        return ""

    if len(body) <= MAX_BODY_CHARS_FOR_SUMMARY:
        return body

    return body[:MAX_BODY_CHARS_FOR_SUMMARY] + "\n...(truncated)"


def summarize_email(subject: str, body: str, model: str) -> str:
    """
    Returns a concise 2-4 sentence summary of the email.

    Falls back to a short notice string if the body is empty -- there is
    nothing meaningful to summarize for an email with no content (e.g.
    Gmail body extraction failed and only an empty snippet remained).
    """

    cleaned_body = _truncate_body((body or "").strip())

    if not cleaned_body:
        return "(No content available to summarize.)"

    prompt = f"""
You are an Email Summarization Agent.

Summarize the email below in 2 to 4 short sentences. Focus only on what
the email is actually about and any action the recipient needs to take.
Do not invent details that are not in the email. Do not include greetings,
signatures, disclaimers, or unsubscribe text in the summary. Write in
plain prose, no bullet points, no headers, no preamble like "This email is
about...".

Email Subject:
{subject}

Email Body:
{cleaned_body}

Summary:
"""

    raw_response = ask_ollama(prompt, model, num_predict=SUMMARY_NUM_PREDICT)
    return raw_response.strip()
