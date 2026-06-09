from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Backend API para FundApp — plataforma de voluntariado y donaciones",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ─────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # En producción reemplaza con tu dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Exception Handler for debugging ──────────────────────────────────────────
from fastapi import Request
from fastapi.responses import JSONResponse
import traceback

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print("GLOBAL EXCEPTION:")
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal Server Error",
            "error_type": type(exc).__name__,
            "error_message": str(exc),
            "traceback": "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
        }
    )

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(router)



# ── Health check ──────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "app": settings.app_name, "version": settings.app_version}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}
