# Marie — Legal AI Phone Assistant Dashboard

A full-stack proof-of-concept dashboard for lawyers to review and act on calls handled by Marie, an AI phone assistant. Built with Django, Django REST Framework, Vue 3, TypeScript, and Tailwind CSS.

---

## Architecture


marie-poc/
  backend/        # Django + DRF + SQLite
  frontend/       # Vite + Vue 3 + TypeScript + Tailwind
  data/
    recordings/   # wav files (not tracked in git — see setup)
    ground_truth.json


### Import pipeline


WAV file
  ↓
Whisper (local) — transcription
  ↓
GPT-4o-mini — extract caller_type, summary, urgent, requires_appointment
  ↓
If urgent → flag in dashboard
If requires_appointment → send follow-up email via Mailtrap with proposed slot


---

## Prerequisites

- Python 3.10+
- Node 18+
- ffmpeg (`brew install ffmpeg` on Mac)
- OpenAI API key
- Mailtrap account (free)

---

## Setup

### 1. Clone the repo

bash
git clone <repo-url>
cd marie-poc


### 2. Place recordings

Copy the provided wav files into:

data/recordings/


### 3. Backend

bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


Create a `.env` file in the `backend/` folder:


OPENAI_API_KEY=your-openai-key
MAILTRAP_HOST=sandbox.smtp.mailtrap.io
MAILTRAP_PORT=2525
MAILTRAP_USER=your-mailtrap-user
MAILTRAP_PASSWORD=your-mailtrap-password


Run migrations:

bash
python3 manage.py migrate


Run the import pipeline (transcribes audio, extracts info, sends emails):

bash
python3 manage.py import_calls ../data/ground_truth.json ../data/recordings


This will take a few minutes — Whisper transcribes each of the 30 wav files locally.

Start the backend:

bash
python3 manage.py runserver


### 4. Frontend

bash
cd frontend
npm install
npm run dev


Open `http://localhost:5173`

---

## Running tests

bash
cd backend
source venv/bin/activate
python3 manage.py test calls


---

## Killer feature — Automated intake action engine

### What it is

After every call, the system analyses the transcript and takes an automated action — exactly what a legal secretary would do:

- **Urgent call** — flagged immediately in the dashboard with a red indicator. The lawyer sees it the moment they log in and knows to call back.
- **Non-urgent call where the caller left an email** — a follow-up email is sent automatically with a proposed appointment slot (next business day at 10am) and a reschedule link.
- **No email left** — logged only, no action taken.

### Why it matters

Every other voice bot gives lawyers a transcript. Marie gives them a decision. The lawyer opens the dashboard in the morning and the intake work is already done — urgent matters are surfaced, follow-up emails are sent, appointments are proposed. No manual triage required.

This is the secretary analogy realised in software.

### KPIs it drives

- **Lead conversion** — callers who leave a voicemail typically never hear back. An automated follow-up email sent within minutes dramatically increases the chance they book a consultation.
- **Time saved per lawyer per month** — no manual review of every call to decide what to do next. The system decides and acts.
- **NPS** — callers feel taken care of immediately, even at 2am.

### How to validate in production

- **A/B test** — 50% of calls get automated follow-up, 50% get the current experience (transcript only). Measure appointment booking rate and lead conversion.
- **Time-to-response metric** — track how long it takes a lawyer to act on a call with vs without the feature.
- **Email open and click rate** — measures whether callers are engaging with the follow-up.
- **User interviews** — ask lawyers after 2 weeks whether they trust the automated emails or feel the need to review them first.

### Production next steps

- Replace proposed slot with Calendly API — book a real slot and send a reschedule link
- Add SMS follow-up for callers who didn't leave an email but left a phone number
- Let lawyers configure urgency rules (e.g. always escalate criminal matters)
- Multi-lawyer firm support — route follow-ups to the right lawyer by practice area

---

## Trade-offs and limitations

- **Whisper `base` model** — fast and runs on CPU but less accurate than `large`. In production, use `large-v3` or a hosted ASR service.
- **SQLite** — right for a local POC, would use PostgreSQL in production.
- **Random `called_at` timestamps** — real timestamps would come from the telephony provider API.
- **Mailtrap** — catches emails locally for demo purposes. Production would use a real provider (Zoho, SendGrid).
- **OpenAI API key required** — the import pipeline calls GPT-4o-mini for extraction. The reviewer needs their own key in `.env`. The dashboard itself runs without it once the import is done.

## Running tests

### Backend
```bash
cd backend
source venv/bin/activate
python3 manage.py test calls
```

### Frontend
```bash
cd frontend
npm run test
```