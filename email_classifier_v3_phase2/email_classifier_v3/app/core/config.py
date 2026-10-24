"""
config.py

Centralized application configuration.

All file paths, scopes, and environment-driven settings live here so that
no other module hardcodes a path or scope string. If you ever need to
change where token.json lives, or which Gmail scope is requested, this
is the only file that needs to change.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# --- Paths -------------------------------------------------------------

# Directory of the project root (this file is at app/core/config.py,
# so go up three levels: core -> app -> project root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Path to the OAuth2 client secrets file downloaded from Google Cloud Console.
# This file identifies YOUR app to Google. It is not user-specific.
CREDENTIALS_FILE = os.getenv(
    "GOOGLE_CREDENTIALS_FILE",
    os.path.join(BASE_DIR, "credentials.json"),
)

# Path where the user's OAuth token (access + refresh token) is cached
# after a successful login. This file IS user-specific and must never
# be committed to version control.
TOKEN_FILE = os.getenv(
    "GOOGLE_TOKEN_FILE",
    os.path.join(BASE_DIR, "token.json"),
)

# --- OAuth settings ------------------------------------------------------

# Gmail readonly scope only. We never request modify/send/delete scopes
# because this application must never alter the mailbox.
GMAIL_SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

# Where Google redirects back to after the user grants/denies consent.
# This MUST exactly match a redirect URI registered for this OAuth
# client in the Google Cloud Console.
OAUTH_REDIRECT_URI = os.getenv(
    "OAUTH_REDIRECT_URI",
    "http://localhost:8000/auth/callback",
)

# --- App settings --------------------------------------------------------

APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", "8000"))

# Gmail API query used by /emails/fetch.
# is:unread          -> only unread mail
# newer_than:1d      -> received within the last 24 hours
GMAIL_FETCH_QUERY = os.getenv("GMAIL_FETCH_QUERY", "is:unread newer_than:1d")

# Maximum number of emails to pull back in a single /emails/fetch call.
GMAIL_FETCH_MAX_RESULTS = int(os.getenv("GMAIL_FETCH_MAX_RESULTS", "25"))
