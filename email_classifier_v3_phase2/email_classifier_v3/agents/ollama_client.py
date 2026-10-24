import ollama
import re

# Network/read timeout (seconds) for a single Ollama request. Without this,
# a slow or stuck Ollama daemon hangs the calling FastAPI request forever.
OLLAMA_TIMEOUT_SECONDS = 30

# If a request times out or the connection fails, retry exactly once before
# giving up. This absorbs the occasional cold-start/slow-load hiccup without
# risking a long hang (worst case: ~2x OLLAMA_TIMEOUT_SECONDS).
OLLAMA_MAX_ATTEMPTS = 2


class OllamaTimeoutError(Exception):
    """Raised when Ollama does not respond within OLLAMA_TIMEOUT_SECONDS
    after exhausting retries."""


def _get_client():
    # Built fresh per call (cheap) so a custom timeout can be supplied;
    # the module-level ollama.chat() helper does not expose a timeout knob.
    return ollama.Client(timeout=OLLAMA_TIMEOUT_SECONDS)


def ask_ollama(prompt, model, num_predict=10):
    last_error = None

    for attempt in range(1, OLLAMA_MAX_ATTEMPTS + 1):
        try:
            client = _get_client()
            response = client.chat(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                options={
                    "temperature": 0,
                    "num_predict": num_predict,
                },
            )
            return response["message"]["content"].strip()

        except Exception as error:
            # ollama-python raises httpx.TimeoutException on timeout and
            # ConnectionError-style exceptions when the daemon is unreachable.
            # Either is worth a single retry; anything else still gets one
            # retry too, since a transient failure shouldn't be distinguished
            # from a timeout from the caller's point of view.
            last_error = error

    raise OllamaTimeoutError(
        f"Ollama request failed after {OLLAMA_MAX_ATTEMPTS} attempt(s): {last_error}"
    )


def sanitize_yes_no(raw_response):
    text = raw_response.strip().lower()

    first_word = re.sub(r"[^a-z]", " ", text).split()

    if first_word:
        if first_word[0] == "yes":
            return "YES"
        if first_word[0] == "no":
            return "NO"

    if re.search(r"\byes\b", text):
        return "YES"

    if re.search(r"\bno\b", text):
        return "NO"

    return "NO"