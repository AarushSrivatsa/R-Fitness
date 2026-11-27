from fastapi import FastAPI

app = FastAPI(
    title="R Fitness API",
    version="0.1.0",
    description="Backend API for the R Fitness website.",
)


@app.get("/healthz", tags=["health"])
async def healthz() -> dict[str, str]:
    """Lightweight health check for deployment platforms."""
    return {"status": "ok"}
