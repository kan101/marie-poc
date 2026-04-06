# Marie — Legal AI Phone Assistant Dashboard

A full-stack proof-of-concept dashboard for lawyers to review and act on calls handled by Marie, an AI phone assistant. Built with Django, Django REST Framework, Vue 3, TypeScript, and Tailwind CSS.

---

## Architecture
```
marie-poc/
  backend/        # Django + DRF + SQLite
  frontend/       # Vite + Vue 3 + TypeScript + Tailwind
  data/
    recordings/   # wav files (not tracked in git — see setup)
    ground_truth.json
```

### Import pipeline

```
WAV file
  ↓
Whisper (local) — transcribes audio to text, runs on CPU, no API key needed
  ↓
GPT-4o-mini — extracts caller_type, summary, urgency, requires_appointment
  ↓
Urgent → flagged in dashboard for immediate callback
Requires appointment → follow-up email sent via Mailtrap with proposed slot
```

---

## Prerequisites

- Python 3.10+
- Node 18+
- ffmpeg (`brew install ffmpeg` on Mac)
- OpenAI API key
- Mailtrap account (free at mailtrap.io)

---

## Setup

### 1. Clone the repo
```
bash
git clone <repo-url>
cd marie-poc
```

### 2. Place recordings

Copy the provided wav files into:

```
data/recordings/
```

### 3. Backend
```
bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in `backend/`:

```
OPENAI_API_KEY=your-openai-key
MAILTRAP_HOST=sandbox.smtp.mailtrap.io
MAILTRAP_PORT=2525
MAILTRAP_USER=your-mailtrap-user
MAILTRAP_PASSWORD=your-mailtrap-password
```

Run migrations:
```
bash
python3 manage.py migrate
```

Run the import pipeline — transcribes all 30 calls, extracts structured data, sends follow-up emails:
```
bash
python3 manage.py import_calls ../data/ground_truth.json ../data/recordings
```

This takes a few minutes. Whisper runs locally.

Start the backend:
```
bash
python3 manage.py runserver
```

### 4. Frontend
```
bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`

---

## Running tests

### Backend
```
bash
cd backend
source venv/bin/activate
python3 manage.py test calls
```

### Frontend
```
bash
cd frontend
npm run test
```

---

## Killer feature — Automated intake action engine

### What it is

After every call, Marie analyses the transcript and takes the action a legal secretary would take:

- **Urgent call** — flagged immediately in the dashboard with a callback badge. The lawyer sees it the moment they log in and knows to prioritise.
- **Caller left an email** — a follow-up email is sent automatically with a proposed appointment slot (next business day at 10am Berlin time) and a reschedule link. Appointment time is displayed on the call card.
- **No email left** — logged only, no action taken.

Every call ends with a clear next step. The lawyer opens the dashboard in the morning and the intake work is already done.

### Why it matters

One of a the fundamental roles of a secretary is to take calls and schedule meetings. This is precisely what Marie does. 

The secretary analogy: a good secretary doesn't wait for the lawyer to read every message before deciding what to do next. They handle it — escalate the urgent ones, follow up on the rest. Marie does the same, automatically, for every call that comes in after hours.

### KPIs it drives

- **Lead conversion** — callers who leave a voicemail and never hear back are lost leads. An automated follow-up sent within minutes of the call dramatically increases the chance they book a consultation.
- **Time saved per lawyer per month** — no manual triage of overnight calls. The system decides and acts.
- **NPS** — callers feel taken care of immediately, even at 2am. A professional follow-up email sets the tone before the lawyer even wakes up.

### How to validate in production

- **A/B test** — 50% of calls get automated follow-up, 50% get transcript only. Measure appointment booking rate and lead conversion over 30 days.
- **Time-to-response metric** — track how long it takes a lawyer to act on a call with vs without the feature.
- **Email engagement** — open rate and reschedule link click rate tells you whether callers are engaging with the follow-up.
- **User interviews** — ask lawyers after 2 weeks whether they trust the automated emails or feel the need to review them first. This informs whether to add an approval step.

### Production next steps

- Replace proposed slot with Calendly API (or similar)— book a real slot and send a genuine reschedule link
- Add SMS follow-up for callers who didn't leave an email but left a phone number
- Let lawyers configure urgency rules per practice area (e.g. always escalate criminal matters)
- Multi-lawyer firm support — route follow-ups to the right lawyer based on matter type
- Add authentication — JWT or session auth so each lawyer sees only their own calls

---

## Technical decisions and trade-offs

| Decision                          | Rationale                                   | Production alternative                         |
|----------------------------------|---------------------------------------------|-----------------------------------------------|
| Whisper `base` model             | Fast, runs on CPU, no API key               | `large-v3` or hosted ASR for better accuracy  |
| SQLite                           | Zero setup for reviewer                     | PostgreSQL                                    |
| Mailtrap                         | Catches emails safely during demo           | SendGrid, or AWS SES                    |
| Random `called_at` timestamps    | Recordings have no real timestamps          | Telephony provider API                        |
| OpenAI API key in `.env`         | Reviewer supplies their own key             | Same pattern in production                    |
| No authentication                | Out of scope for POC                        | JWT via djangorestframework-simplejwt         |
| `gpt-4o-mini` for extraction     | Fast and cheap, sufficient for structured JSON | Fine-tuned model for legal domain accuracy |

---

## Project structure

```
backend/
  calls/
    management/
      commands/
        import_calls.py   # import pipeline: transcribe → extract → email
    models.py             # Caller and Call models
    serializers.py        # list, detail, and notes serializers
    views.py              # REST endpoints
    tests.py              # 22 backend tests
  config/
    settings.py

frontend/
  src/
    components/
      Badge.vue           # reusable pill badge
      CallCard.vue        # individual call card with audio player
      CallFilters.vue     # search and filter toolbar
      CallDetailModal.vue # full call detail with transcript and notes
      StatsBar.vue        # summary metrics
    views/
      Dashboard.vue       # main layout
    api.ts                # typed API client
    __tests__/            # 33 frontend tests

```