# R Fitness

A gym website and lead-management dashboard for R Fitness, Uppal, Hyderabad.

## Stack

- Frontend: Vue 3, TypeScript, Vite, Bootstrap 5
- API: FastAPI, Pydantic, SQLAlchemy 2, Alembic
- Database: Neon PostgreSQL
- Admin authentication: app-managed email/password login, Argon2 password hashing, signed JWTs
- Hosting: Render static site + Docker web service

## Repository layout

```text
frontend/       Vue website and admin dashboard
backend/        FastAPI application, migrations and tests
render.yaml     Render Blueprint for frontend + API
```

## Local development

### Backend

Python 3.12+ is recommended.

```bash
cd backend
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
cp .env.example .env
```

Set `DATABASE_URL` to the Neon PostgreSQL connection string. Use the Neon pooled connection string and keep `sslmode=require` enabled. The app adapts standard `postgresql://` URLs to psycopg.

Generate the admin password hash locally. The command prompts for the password without echoing it:

```bash
python -c "from getpass import getpass; from pwdlib import PasswordHash; print(PasswordHash.recommended().hash(getpass('Admin password: ')))"
```

Generate a JWT signing secret:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Put the generated hash in `ADMIN_PASSWORD_HASH` and the random value in `JWT_SECRET`. Configure `ADMIN_EMAIL` with the admin login email. Never commit real credentials or `.env` files.

```bash
alembic upgrade head
uvicorn app.main:app --reload
```

API docs: http://localhost:8000/docs  
Health check: http://localhost:8000/healthz

### Frontend

In a second terminal:

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Open http://localhost:5173. Set `VITE_API_BASE_URL=http://localhost:8000`.

## Neon database setup

1. Create a Neon project and database.
2. Copy the pooled connection string from the Neon dashboard. Keep `sslmode=require` in the URL.
3. Add the connection string as `DATABASE_URL` in the backend environment.
4. Run `alembic upgrade head` locally, or let the Render Docker entrypoint apply migrations during deployment.

The database schema is managed through Alembic. The app accesses Neon through the FastAPI backend; the browser never connects directly to PostgreSQL.

## Admin authentication

- The admin login endpoint is `POST /api/v1/auth/login`.
- The admin email is configured by `ADMIN_EMAIL`.
- Only an Argon2 password hash is stored in `ADMIN_PASSWORD_HASH`; the original password is never stored.
- `JWT_SECRET` signs access tokens. Use a unique random value of at least 32 characters.
- Tokens expire after eight hours. The dashboard keeps the token in the current browser tab's session storage.
- All admin API routes validate the signed token server-side.

Use a long, unique admin password. Keep `ADMIN_PASSWORD_HASH` and `JWT_SECRET` private and only configure them on the backend service.

## Render deployment

The root `render.yaml` defines:
- `r-fitness-web`: Vue static site
- `r-fitness-api`: FastAPI Docker web service

Required API variables:

| Variable | Value |
|---|---|
| `DATABASE_URL` | Neon PostgreSQL pooled connection string |
| `ADMIN_EMAIL` | Admin sign-in email |
| `ADMIN_PASSWORD_HASH` | Argon2 hash generated locally |
| `JWT_SECRET` | Random secret generated locally |
| `CORS_ORIGINS` | Exact deployed frontend origin, e.g. `https://r-fitness-web.onrender.com` |
| `APP_ENV` | Already set to `production` in `render.yaml` |

Required frontend variable:

| Variable | Value |
|---|---|
| `VITE_API_BASE_URL` | Deployed API origin, e.g. `https://r-fitness-api.onrender.com` |

No database credentials or admin secrets belong in frontend variables. The API container applies Alembic migrations before starting Uvicorn. Render health checks use `/healthz`.

## Before publishing

The initial content uses the public business listing for the gym's name, address and phone. Confirm these with the owner before launch. Membership prices, exact services, trainer profiles, class schedules and Sunday hours are intentionally not invented; populate them after the owner confirms the details. Replace representative stock photos with original R Fitness photographs before publishing.

## MVP included

- Responsive public gym website
- Membership plans (no invented prices)
- Trial / membership enquiry form stored in PostgreSQL
- App-managed administrator login with Argon2 and JWT
- Admin enquiry inbox with status updates
- Admin membership-plan management
- Docker, database migrations, health check and Render Blueprint

Member accounts, payments, attendance, trainer management UI and class booking are future phases.
