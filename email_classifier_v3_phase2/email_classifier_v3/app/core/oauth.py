"""
oauth.py

Encapsulates all Google OAuth2 mechanics:

- Building the Flow object from credentials.json
- Generating the authorization URL the user is redirected to
- Exchanging the authorization code (from Google's callback) for a token
- Persisting the token to token.json
- Loading a cached token from disk, refreshing it silently if expired

Nothing in this file talks HTTP directly to the browser/client — that is
the router's job. This module only knows about Google's OAuth/Gmail
client libraries.
"""

from typing import Optional
import os
import os
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request as GoogleAuthRequest
from google_auth_oauthlib.flow import Flow

from app.core.config import (
    CREDENTIALS_FILE,
    TOKEN_FILE,
    GMAIL_SCOPES,
    OAUTH_REDIRECT_URI,
)


class OAuthConfigError(Exception):
    """Raised when credentials.json is missing or malformed."""
    pass


def _ensure_credentials_file_exists():
    if not os.path.exists(CREDENTIALS_FILE):
        raise OAuthConfigError(
            f"credentials.json not found at '{CREDENTIALS_FILE}'. "
            "Download it from Google Cloud Console (APIs & Services > "
            "Credentials > OAuth 2.0 Client ID > Desktop or Web app) "
            "and place it at the project root."
        )


def build_flow() -> Flow:
    """
    Construct a google_auth_oauthlib Flow configured for this app.
    """
    _ensure_credentials_file_exists()

    flow = Flow.from_client_secrets_file(
        CREDENTIALS_FILE,
        scopes=GMAIL_SCOPES,
        redirect_uri=OAUTH_REDIRECT_URI,
    )
    return flow


def get_authorization_url() -> str:
    """
    Returns the Google consent screen URL.
    """
    flow = build_flow()

    auth_url, _state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )
    return auth_url


def exchange_code_for_credentials(authorization_response_url: str) -> Credentials:
    """
    Exchange authorization code for credentials.
    """
    flow = build_flow()
    flow.fetch_token(authorization_response=authorization_response_url)
    return flow.credentials


def save_credentials(credentials: Credentials) -> None:
    """
    Persist credentials to token.json
    """
    with open(TOKEN_FILE, "w") as token_file:
        token_file.write(credentials.to_json())


def load_credentials() -> Optional[Credentials]:
    """
    Load cached credentials from token.json.
    """
    if not os.path.exists(TOKEN_FILE):
        return None

    credentials = Credentials.from_authorized_user_file(
        TOKEN_FILE,
        GMAIL_SCOPES
    )

    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(GoogleAuthRequest())
        save_credentials(credentials)

    return credentials


def is_authenticated() -> bool:
    """
    True if valid token exists.
    """
    credentials = load_credentials()
    return bool(credentials and credentials.valid)