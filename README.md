# Email Classifier V3

A local AI-powered Gmail priority dashboard that fetches unread Gmail emails, classifies them using a local Ollama model, displays them in a React dashboard, and exports results as CSV and Markdown digest files.

This project was built as a production-style upgrade from an earlier IMAP-based local email classifier.

---

## 1. What This Project Does

Email Classifier V3 helps users manage unread Gmail messages by automatically sorting emails into an Eisenhower Matrix priority system:

1. Urgent + Important
2. Important, Not Urgent
3. Urgent, Not Important
4. Neither

The system uses:

* Gmail API with OAuth2 authentication
* FastAPI backend
* React + Vite + Tailwind frontend
* Ollama local LLM classification
* CSV export
* Markdown digest export
* Persistent JSON logging
* One-click launcher
* PyInstaller executable launcher

---

## 2. Why V3 Was Built

The original system used IMAP login with Gmail App Passwords.

However, Gmail began restricting repeated IMAP login attempts, which caused the test account to be suspended. Because of this, the project was migrated to a more production-ready architecture using Gmail API and OAuth2.

### Old System

```text
Python IMAP login
↓
Fetch unread emails
↓
Ollama classification
↓
HTML/CSV output
```

### New V3 System

```text
React Frontend
↓
FastAPI Backend
↓
Google OAuth2
↓
Gmail API
↓
Ollama Local AI
↓
Dashboard + CSV + Markdown + Logs
```

---

## 3. Main Features

### Gmail OAuth2 Authentication

The app uses Google OAuth2 instead of IMAP password login.

Features:

* Secure Google sign-in
* OAuth token stored locally in `token.json`
* No repeated Gmail password login
* Logout button deletes saved token
* Gmail API used for email access

---

### Live Gmail Fetching

The backend fetches unread Gmail emails using the Gmail API.

Fetched email fields include:

* Gmail message ID
* Sender
* Subject
* Date
* Snippet / preview text

---

### Local AI Classification

The app uses Ollama running locally on the user's machine.

Current model used:

```text
qwen2.5:3b
```

The system uses an agentic classification pipeline:

```text
Email
↓
Urgency Agent
↓
Importance Agent
↓
Coordinator
↓
Eisenhower Matrix Category
```

---

### Classification Categories

#### Urgent + Important

Emails that need quick action and also matter.

Examples:

* Reply required within 48 hours
* Security alerts
* Payment failures
* Internship/client/project deadlines
* Academic deadlines
* Important official messages

#### Important, Not Urgent

Emails that matter but do not need immediate action.

Examples:

* Future project discussions
* Internship updates
* Academic information
* Interview opportunities without immediate deadline

#### Urgent, Not Important

Emails that are time-sensitive but low value.

Examples:

* OTPs
* Delivery alerts
* Minor reminders
* Automated confirmations

#### Neither

Low-value or non-actionable messages.

Examples:

* Promotions
* Newsletters
* Ads
* Social notifications
* LinkedIn profile view alerts

---

## 4. Project Folder Structure

The project root folder is:

```text
email/
```

Expected structure:

```text
email/
│
├── launcher.py
├── README.md
├── dist/
│   └── EmailClassifierLauncher.exe
│
├── email_classifier_v3_phase2/
│   └── email_classifier_v3/
│       │
│       ├── main.py
│       ├── credentials.json
│       ├── token.json
│       │
│       ├── logs/
│       │   └── email_classification_log.json
│       │
│       ├── agents/
│       │   ├── ollama_client.py
│       │   ├── urgency_agent.py
│       │   ├── importance_agent.py
│       │   ├── coordinator.py
│       │   └── email_parser.py
│       │
│       └── app/
│           ├── core/
│           │   ├── config.py
│           │   ├── gmail_service.py
│           │   └── oauth.py
│           │
│           ├── routers/
│           │   ├── auth_router.py
│           │   └── emails_router.py
│           │
│           └── services/
│               ├── classifier_service.py
│               ├── digest_service.py
│               └── log_service.py
│
└── email_classifier_frontend_redesigned/
    │
    ├── package.json
    ├── index.html
    ├── vite.config.js
    ├── tailwind.config.js
    │
    └── src/
        ├── main.jsx
        ├── App.jsx
        │
        ├── lib/
        │   └── api.js
        │
        ├── hooks/
        │   └── useInboxPolling.js
        │
        ├── pages/
        │   └── Dashboard.jsx
        │
        └── components/
            ├── Sidebar.jsx
            ├── Header.jsx
            ├── ConnectPanel.jsx
            ├── EmailList.jsx
            ├── EmailCard.jsx
            ├── InsightPanel.jsx
            ├── CategoryGrid.jsx
            └── ExportBar.jsx
```

---

## 5. Backend Overview

Backend folder:

```text
email_classifier_v3_phase2/email_classifier_v3/
```

The backend is built using FastAPI.

### Main Backend File

```text
main.py
```

This starts the FastAPI application and includes routers.

---

### Auth Router

File:

```text
app/routers/auth_router.py
```

Endpoints:

```text
GET  /auth/login
GET  /auth/callback
GET  /auth/status
POST /auth/logout
```

Purpose:

* `/auth/login` redirects user to Google OAuth screen
* `/auth/callback` receives Google OAuth code and saves token
* `/auth/status` checks if Gmail is connected
* `/auth/logout` deletes `token.json` and disconnects Gmail

---

### Emails Router

File:

```text
app/routers/emails_router.py
```

Endpoints:

```text
GET    /emails/fetch
GET    /emails/export/csv
GET    /emails/export/md
GET    /emails/logs
DELETE /emails/logs
```

Purpose:

* `/emails/fetch` fetches unread emails and classifies them
* `/emails/export/csv` downloads classified emails as CSV
* `/emails/export/md` downloads a Markdown digest
* `/emails/logs` returns saved classification logs
* `DELETE /emails/logs` clears logs

---

### Gmail Service

File:

```text
app/core/gmail_service.py
```

Purpose:

* Loads saved OAuth credentials
* Creates Gmail API service client
* Throws authentication error if token is missing

---

### OAuth Logic

File:

```text
app/core/oauth.py
```

Purpose:

* Builds Google OAuth flow
* Generates Google authorization URL
* Exchanges callback code for credentials
* Saves credentials to `token.json`
* Checks authentication status

Important local development setting:

```python
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
```

This allows OAuth over local HTTP during development.

Production apps should use HTTPS.

---

### Config

File:

```text
app/core/config.py
```

Purpose:

Stores Gmail fetch settings such as:

```text
GMAIL_FETCH_QUERY
GMAIL_FETCH_MAX_RESULTS
```

Example query:

```text
is:unread
```

---

## 6. AI Agent Files

Folder:

```text
agents/
```

### Ollama Client

File:

```text
agents/ollama_client.py
```

Purpose:

* Sends prompts to local Ollama model
* Uses deterministic output settings
* Sanitizes YES/NO responses

---

### Urgency Agent

File:

```text
agents/urgency_agent.py
```

Purpose:

Determines if an email is urgent.

Returns:

```text
YES
NO
```

Urgency signals include:

* urgent
* asap
* reply within 48 hours
* action required
* deadline
* due today/tomorrow
* security warning
* payment due
* account locked

Promotional fake urgency is ignored.

Example:

```text
"KFC offer ends today"
```

should not be treated as truly urgent.

---

### Importance Agent

File:

```text
agents/importance_agent.py
```

Purpose:

Determines if an email is important.

Returns:

```text
YES
NO
```

Importance signals include:

* work
* internship
* project
* academic messages
* payment issues
* security/account alerts
* official documents
* direct reply requests
* recruiter/interview messages

Low-value social notifications are ignored unless they involve real opportunity or action.

---

### Coordinator

File:

```text
agents/coordinator.py
```

Purpose:

Combines urgency and importance into final category.

Logic:

```text
Urgent YES + Important YES → urgent-important
Urgent NO  + Important YES → important-not-urgent
Urgent YES + Important NO  → urgent-not-important
Urgent NO  + Important NO  → neither
```

---

## 7. Backend Services

Folder:

```text
app/services/
```

### Classifier Service

File:

```text
classifier_service.py
```

Purpose:

* Takes Gmail email data
* Runs urgency agent
* Runs importance agent
* Runs coordinator
* Returns enriched classified email data

Adds fields:

```text
urgency
importance
classification
classification_label
classification_error
```

---

### Log Service

File:

```text
log_service.py
```

Purpose:

Stores classification results in a local JSON log file.

Log file path:

```text
logs/email_classification_log.json
```

Each log entry stores:

* logged time
* Gmail message ID
* date
* sender
* subject
* snippet
* urgency
* importance
* classification
* classification label
* classification error

Duplicate emails are avoided using Gmail message ID.

---

### Digest Service

File:

```text
digest_service.py
```

Purpose:

Generates Markdown digest reports from classified emails.

Digest groups emails by:

* Urgent + Important
* Important, Not Urgent
* Urgent, Not Important
* Neither
* Unclassified / Errors

---

## 8. Frontend Overview

Frontend folder:

```text
email_classifier_frontend_redesigned/
```

Frontend stack:

```text
React
Vite
Tailwind CSS
```

---

### Main Dashboard

File:

```text
src/pages/Dashboard.jsx
```

Purpose:

* Loads authentication state
* Shows Connect Gmail screen if not authenticated
* Shows main dashboard after Gmail is connected
* Displays emails and insight panel

---

### Polling Hook

File:

```text
src/hooks/useInboxPolling.js
```

Purpose:

* Calls `/auth/status`
* Calls `/emails/fetch`
* Polls inbox repeatedly
* Updates dashboard with latest unread emails
* Tracks loading state, error state, and last sync time

---

### API Helper

File:

```text
src/lib/api.js
```

Purpose:

Central place for frontend backend API URLs.

Includes functions for:

```text
getLoginUrl()
getCsvExportUrl()
getMarkdownExportUrl()
fetchAuthStatus()
fetchUnreadEmails()
logout()
```

---

### Header

File:

```text
src/components/Header.jsx
```

Purpose:

* Shows title
* Shows last sync time
* Shows Gmail connected/disconnected state
* Refresh button
* Logout button

---

### Connect Panel

File:

```text
src/components/ConnectPanel.jsx
```

Purpose:

Shown when Gmail is not connected.

The user clicks Connect Gmail, which opens:

```text
/auth/login
```

---

### Email List

File:

```text
src/components/EmailList.jsx
```

Purpose:

Displays classified email cards.

Handles:

* Loading state
* Error state
* Empty inbox state

---

### Email Card

File:

```text
src/components/EmailCard.jsx
```

Purpose:

Displays each email with:

* sender
* subject
* snippet
* urgency badge
* importance badge
* category badge
* classification error if any

---

### Insight Panel

File:

```text
src/components/InsightPanel.jsx
```

Purpose:

Right-side dashboard panel showing:

* total unread emails fetched
* number of matrix lanes
* category grid
* export buttons

---

### Category Grid

File:

```text
src/components/CategoryGrid.jsx
```

Purpose:

Shows count of emails in each Eisenhower category.

Counts are dynamic and based on email classification.

---

### Export Bar

File:

```text
src/components/ExportBar.jsx
```

Purpose:

Provides export buttons:

```text
CSV Export
Markdown Digest
HTML Report soon
```

---

## 9. Launcher Overview

File:

```text
launcher.py
```

Purpose:

Starts the full application with one command or one executable.

It starts:

```text
Ollama
FastAPI backend
React frontend
Browser dashboard
```

It checks ports:

```text
11434 → Ollama
8000  → FastAPI backend
5173  → React frontend
```

Expected behavior:

```text
Double click launcher
↓
Ollama starts or is detected
↓
Backend starts
↓
Frontend starts
↓
Browser opens http://localhost:5173
```

---

## 10. Executable Launcher

The launcher can be packaged into an executable using PyInstaller.

Command:

```powershell
cd C:\Users\pranj\Desktop\email
python -m PyInstaller --onefile --name EmailClassifierLauncher launcher.py
```

Output:

```text
dist/EmailClassifierLauncher.exe
```

Run:

```text
dist/EmailClassifierLauncher.exe
```

Important:

The executable expects the project folders to remain one level above `dist`.

Expected layout:

```text
email/
├── dist/
│   └── EmailClassifierLauncher.exe
├── email_classifier_v3_phase2/
└── email_classifier_frontend_redesigned/
```

---

## 11. Requirements

### Backend Requirements

Python 3.9+ recommended.

Install backend dependencies:

```powershell
pip install fastapi uvicorn google-auth google-auth-oauthlib google-api-python-client requests ollama
```

If direct commands fail on Windows, use:

```powershell
python -m pip install fastapi uvicorn google-auth google-auth-oauthlib google-api-python-client requests ollama
```

---

### Frontend Requirements

Node.js and npm required.

Install frontend dependencies:

```powershell
cd email_classifier_frontend_redesigned
npm install
```

---

### Ollama Requirements

Install Ollama from:

```text
https://ollama.com
```

Pull the model:

```powershell
ollama pull qwen2.5:3b
```

Check installed models:

```powershell
ollama list
```

Expected:

```text
qwen2.5:3b
```

---

## 12. Google Cloud Setup

This project requires Gmail API OAuth credentials.

### Step 1: Create Google Cloud Project

Go to Google Cloud Console.

Create a project called:

```text
Email Classifier V3
```

---

### Step 2: Enable Gmail API

Go to:

```text
APIs & Services → Library
```

Search:

```text
Gmail API
```

Enable it.

---

### Step 3: Create OAuth Credentials

Go to:

```text
APIs & Services → Credentials
```

Create OAuth Client ID.

Recommended for this local app:

```text
Application Type: Desktop App
```

Download the JSON file.

Rename it:

```text
credentials.json
```

Place it here:

```text
email_classifier_v3_phase2/email_classifier_v3/credentials.json
```

---

### Step 4: Add Test User

If app is in testing mode, add your Gmail account as a test user.

Go to:

```text
Google Auth Platform → Audience → Test Users
```

Add the Gmail address being used.

---

### Step 5: Local OAuth Note

For localhost development, the backend allows insecure local HTTP OAuth using:

```python
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
```

This is for local testing only.

Production deployments should use HTTPS.

---

## 13. Manual Run Instructions

Use this if not using the launcher.

### Terminal 1: Start Ollama

```powershell
ollama serve
```

If Ollama is already running, this may not be required.

---

### Terminal 2: Start Backend

```powershell
cd C:\Users\pranj\Desktop\email\email_classifier_v3_phase2\email_classifier_v3
python -m uvicorn main:app --reload --port 8000
```

Expected:

```text
Uvicorn running on http://127.0.0.1:8000
Application startup complete
```

---

### Terminal 3: Start Frontend

```powershell
cd C:\Users\pranj\Desktop\email\email_classifier_frontend_redesigned
npm run dev
```

Expected:

```text
Local: http://localhost:5173
```

---

### Open App

```text
http://localhost:5173
```

---

## 14. One-Click Run Instructions

Preferred method after setup:

```text
Double click dist/EmailClassifierLauncher.exe
```

The launcher will:

* detect/start Ollama
* start backend
* start frontend
* open browser automatically

---

## 15. How to Use the App

### First Time

1. Run launcher or start app manually.
2. Open dashboard.
3. Click Connect Gmail.
4. Complete Google OAuth sign-in.
5. Return to dashboard.
6. Emails will be fetched and classified.

---

### Normal Use

1. Start app.
2. Dashboard opens automatically.
3. Click Refresh if needed.
4. Review classified emails.
5. Export CSV or Markdown digest if required.

---

### Logout

Click:

```text
Logout
```

This deletes:

```text
token.json
```

After logout, the app returns to the Connect Gmail screen.

---

## 16. Export Features

### CSV Export

Button:

```text
CSV Export
```

Endpoint:

```text
GET /emails/export/csv
```

Downloads:

```text
email_classifier_export_YYYYMMDD_HHMMSS.csv
```

CSV fields:

* id
* date
* sender
* subject
* snippet
* urgency
* importance
* classification
* classification_label
* classification_error

---

### Markdown Digest

Button:

```text
Markdown Digest
```

Endpoint:

```text
GET /emails/export/md
```

Downloads:

```text
email_classifier_digest_YYYYMMDD_HHMMSS.md
```

Digest includes:

* generation time
* total emails
* category summary table
* grouped email sections
* sender
* subject
* date
* urgency
* importance
* category
* preview snippet

---

## 17. Logs

Logs are stored automatically.

Path:

```text
email_classifier_v3_phase2/email_classifier_v3/logs/email_classification_log.json
```

View logs in browser:

```text
http://localhost:8000/emails/logs
```

Clear logs:

```text
DELETE http://localhost:8000/emails/logs
```

Logs avoid duplicates using Gmail message ID.

---

## 18. API Endpoint Summary

### Auth

```text
GET  /auth/login
GET  /auth/callback
GET  /auth/status
POST /auth/logout
```

### Emails

```text
GET    /emails/fetch
GET    /emails/export/csv
GET    /emails/export/md
GET    /emails/logs
DELETE /emails/logs
```

---

## 19. Common Errors and Fixes

### `uvicorn is not recognized`

Use:

```powershell
python -m uvicorn main:app --reload --port 8000
```

instead of:

```powershell
uvicorn main:app --reload --port 8000
```

---

### `Could not import module "main"`

You are probably in the wrong folder.

Correct backend folder:

```text
email_classifier_v3_phase2/email_classifier_v3
```

Run backend from there.

---

### `credentials.json not found`

Place the file here:

```text
email_classifier_v3_phase2/email_classifier_v3/credentials.json
```

---

### `JSONDecodeError` for credentials

The credentials file is malformed.

Fix:

* re-download OAuth client JSON
* rename to `credentials.json`
* do not paste extra text into the file

---

### Google OAuth says access denied

Add your Gmail as a test user in Google Auth Platform.

---

### Google OAuth says HTTPS required

For local testing, ensure this is set in OAuth code:

```python
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
```

---

### `No module named pyinstaller`

Use:

```powershell
python -m PyInstaller --onefile --name EmailClassifierLauncher launcher.py
```

not:

```powershell
pyinstaller ...
```

---

### Frontend does not open

Run manually:

```powershell
cd email_classifier_frontend_redesigned
npm run dev
```

Then open:

```text
http://localhost:5173
```

---

### Ollama classification fails

Check if Ollama is running:

```powershell
ollama list
```

If needed:

```powershell
ollama serve
```

Make sure model exists:

```powershell
ollama pull qwen2.5:3b
```

---

## 20. Security Notes

Do not upload these files to GitHub:

```text
credentials.json
token.json
logs/
```

Recommended `.gitignore` entries:

```gitignore
credentials.json
token.json
logs/
dist/
build/
__pycache__/
node_modules/
.env
```

OAuth token files provide access to Gmail and must remain private.

---

## 21. Final Project Status

Completed:

```text
FastAPI backend
React frontend
Gmail OAuth2 authentication
Gmail API unread fetch
Ollama local LLM classification
Urgency agent
Importance agent
Coordinator
Dynamic priority dashboard
CSV export
Markdown digest export
Persistent JSON logs
Logout support
One-click launcher
PyInstaller executable launcher
```

Optional future improvements:

```text
HTML report export
classification caching
desktop shell using Tauri/Electron
system tray support
better app icon
automatic shutdown manager
analytics charts
multi-account Gmail support
database storage
```

---

## 22. One-Line Summary

Email Classifier V3 is a local AI-powered Gmail triage dashboard that securely connects to Gmail using OAuth2, fetches unread emails through Gmail API, classifies them locally with Ollama into Eisenhower Matrix priority categories, and provides dashboard, CSV, Markdown, logging, and executable launcher support.

---
