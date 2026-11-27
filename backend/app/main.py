from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import admin, auth, public

app = FastAPI(
    title="R Fitness API",
    version="0.2.0",
    description="Public website and admin API for R Fitness, Uppal, Hyderabad.",
    docs_url="/docs" if settings.app_env != "production" else None,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.get("/healthz", tags=["health"])
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/", include_in_schema=False)
async def root() -> dict[str, str]:
    return {"name": "R Fitness API", "status": "online"}


app.include_router(auth.router)
app.include_router(public.router)
app.include_router(admin.router)
