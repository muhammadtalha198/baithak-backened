# Deploy on Vercel

Push to GitHub → Vercel auto-deploys. No VPS or Docker needed.

## 1. Connect repo

1. Go to [vercel.com/new](https://vercel.com/new)
2. Import **baithak-backened** from GitHub
3. Framework preset: **Other**
4. Deploy

## 2. Add a Postgres database

Use one of these (all work with Vercel):

| Provider | Free tier |
|----------|-----------|
| [Neon](https://neon.tech) | Yes |
| [Supabase](https://supabase.com) | Yes |
| [Vercel Postgres](https://vercel.com/storage/postgres) | Yes |

Copy the **async** connection string and convert to:

```
postgresql+asyncpg://user:pass@host/dbname?ssl=require
```

## 3. Environment variables (Vercel dashboard)

**Easiest way:** use the import file.

```bash
cp .env.vercel.example .env.vercel
# Edit .env.vercel with your real values
```

In Vercel → **Environment Variables** → **Import .env** → select `.env.vercel`

Or add them one by one:

| Variable | Required | Example |
|----------|----------|---------|
| `DATABASE_URL` | Yes | `postgresql+asyncpg://...?ssl=require` |
| `JWT_SECRET` | Yes | 32+ random characters |
| `FRONTEND_URL` | Yes | `https://baithak-frontened.vercel.app` |
| `FEATURE_LOGIN_ENABLED` | Yes | `true` |
| `REDIS_URL` | No | Upstash Redis URL (optional, for rate limiting) |
| `EARLY_BIRD_LIMIT` | No | `50` |

**Important:** Never commit `.env.vercel` to GitHub — it contains secrets. Only commit `.env.vercel.example`.

## 4. Run database migrations

Add `DATABASE_URL` as a **GitHub secret** in the backend repo, then push to `main` — the **Database Migrations** workflow runs `alembic upgrade head` automatically.

Or run once locally:

```bash
DATABASE_URL="postgresql+asyncpg://..." alembic upgrade head
```

## 5. Verify

```bash
curl https://your-api.vercel.app/health
# {"status":"ok"}
```

## Auto-deploy flow

```
git push origin main  →  Vercel rebuilds  →  live in ~1 min
```

## Optional: Redis (rate limiting)

Create a free [Upstash Redis](https://upstash.com) database and set:

```
REDIS_URL=rediss://default:password@host:6379
```

Without Redis, registration still works — rate limiting is skipped.

## GitHub secrets (migrations only)

| Secret | Purpose |
|--------|---------|
| `DATABASE_URL` | Run Alembic on push |

No SSH or deploy secrets needed — Vercel handles deployment.
