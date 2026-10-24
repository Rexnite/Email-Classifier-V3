"""
main.py

FastAPI application entrypoint.

Run with:
    uvicorn main:app --reload --port 8000

This file only wires routers together. Business logic lives in
app/core (OAuth + Gmail service construction) and app/routers
(HTTP endpoints).
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth_router, emails_router

app = FastAPI(
    title="Gmail AI Classifier - Backend (Phase 1)",
    description=(
        "Phase 1: Google OAuth2 authentication and Gmail API unread-email "
        "fetching. No classification logic yet."
    ),
    version="0.1.0",
)

# Allow the Vite dev frontend to call this API directly from the browser.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(emails_router.router)


@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Gmail AI Classifier backend is running.",
        "next_steps": [
            "GET /auth/login    - start Google OAuth login",
            "GET /auth/status   - check if authenticated",
            "GET /emails/fetch  - fetch unread emails (last 24h)",
        ],
    }
