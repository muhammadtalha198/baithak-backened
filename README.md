# Baithak Backend

FastAPI backend for user registration and login (OTP coming later).

## Quick start (local)

```bash
cd backened
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
docker compose up -d postgres redis
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

## Deploy with Docker

```bash
cp .env.example .env
# Set JWT_SECRET, FRONTEND_URL (your live site URL)
docker compose up -d --build
```

The API runs on port **8000** and runs migrations on startup.

## Environment

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | Postgres async URL |
| `REDIS_URL` | Redis URL (rate limiting) |
| `JWT_SECRET` | Strong random secret (32+ chars) |
| `FRONTEND_URL` | Allowed CORS origin(s), comma-separated |
| `EARLY_BIRD_LIMIT` | First N users get discount (default 50) |

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/auth/register` | Register with name + email or phone + password |
| POST | `/auth/login` | Login with email or phone + password |
| GET | `/auth/me` | Current user (Bearer token) |

### Register example

```json
{
  "name": "Aisha Khan",
  "email": "aisha@example.com",
  "password": "secret123"
}
```

First 50 users get `early_bird_discount: true` automatically.
