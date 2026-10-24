"""
gmail_service.py

Builds an authenticated Gmail API service object using cached
credentials. Every router that needs to talk to Gmail goes through
get_gmail_service() rather than touching googleapiclient directly,
so there is exactly one place that knows how the service is constructed.
"""

from googleapiclient.discovery import build
from googleapiclient.discovery import Resource

from app.core.oauth import load_credentials


class NotAuthenticatedError(Exception):
    """Raised when no valid token is available to build a Gmail service."""


def get_gmail_service() -> Resource:
    """
    Returns an authenticated Gmail API service (v1) ready to use.

    Raises NotAuthenticatedError if the user hasn't completed the
    OAuth login flow yet (no token.json) or the cached token could
    not be refreshed.
    """
    credentials = load_credentials()

    if not credentials or not credentials.valid:
        raise NotAuthenticatedError(
            "No valid Gmail credentials found. Visit /auth/login first."
        )

    # cache_discovery=False avoids writing a discovery cache file to disk,
    # which keeps this app's filesystem footprint predictable.
    service = build("gmail", "v1", credentials=credentials, cache_discovery=False)
    return service
