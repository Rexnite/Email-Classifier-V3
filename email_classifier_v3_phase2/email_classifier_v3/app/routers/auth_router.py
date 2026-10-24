"""
auth_router.py

Exposes the OAuth endpoints:

    GET /auth/login     -> redirects the user's browser to Google's consent screen
    GET /auth/callback  -> Google redirects back here with a `code`
    GET /auth/status    -> checks whether the app currently holds a valid token
    POST /auth/logout   -> deletes token.json and logs the user out
"""

from pathlib import Path

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse

from app.core.oauth import (
    get_authorization_url,
    exchange_code_for_credentials,
    save_credentials,
    is_authenticated,
    OAuthConfigError,
)

router = APIRouter(prefix="/auth", tags=["auth"])

TOKEN_PATH = Path("token.json")


@router.get("/login")
def login():
    """
    Step 1 of OAuth2: send the user's browser to Google's consent screen.
    """
    try:
        authorization_url = get_authorization_url()
    except OAuthConfigError as error:
        raise HTTPException(status_code=500, detail=str(error))

    return RedirectResponse(authorization_url)


@router.get("/callback")
def callback(request: Request):
    """
    Step 2 of OAuth2: Google redirects the user's browser back here with
    `code` and `state` query parameters.

    We reconstruct the full callback URL and exchange it for credentials,
    then save them to token.json for reuse.
    """
    full_callback_url = str(request.url)

    if "error" in request.query_params:
        raise HTTPException(
            status_code=400,
            detail=f"Google OAuth error: {request.query_params['error']}",
        )

    if "code" not in request.query_params:
        raise HTTPException(
            status_code=400,
            detail="Missing 'code' parameter in OAuth callback.",
        )

    try:
        credentials = exchange_code_for_credentials(full_callback_url)
        save_credentials(credentials)
    except OAuthConfigError as error:
        raise HTTPException(status_code=500, detail=str(error))
    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to exchange authorization code for token: {error}",
        )

    return RedirectResponse("http://localhost:5173")


@router.get("/status")
def status():
    """Quick check: does this app currently have a usable Gmail token?"""
    return {"authenticated": is_authenticated()}


@router.post("/logout")
def logout():
    """
    Logs out the connected Gmail account by deleting the saved OAuth token.
    The next frontend refresh will show the Connect Gmail screen again.
    """
    if TOKEN_PATH.exists():
        TOKEN_PATH.unlink()

    return {
        "authenticated": False,
        "message": "Logged out successfully.",
    }