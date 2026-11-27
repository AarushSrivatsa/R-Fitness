from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.routers import admin, auth, public

app = FastAPI(
    title="R Fitness",
    version="0.3.0",
    description="R Fitness website and administration API.",
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


app.include_router(auth.router)
app.include_router(public.router)
app.include_router(admin.router)


class SpaStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        try:
            return await super().get_response(path, scope)
        except StarletteHTTPException as exc:
            if exc.status_code == 404 and not path.startswith(
                ("api/", "healthz", "docs", "openapi.json")
            ):
                return await super().get_response("index.html", scope)
            raise


frontend_dist = Path(__file__).resolve().parent.parent / "frontend-dist"
if frontend_dist.is_dir():
    app.mount("/", SpaStaticFiles(directory=str(frontend_dist), html=True), name="frontend")
else:
    @app.get("/", include_in_schema=False)
    async def root() -> dict[str, str]:
        return {"name": "R Fitness API", "status": "online"}
