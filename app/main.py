import traceback

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from postgrest.exceptions import APIError

from app.api.v1.router import router
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Backend API para FundApp - plataforma de voluntariado y donaciones",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
origins = [
    "https://fund-app-ashen.vercel.app",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _friendly_database_error(exc: APIError) -> tuple[int, str]:
    code = getattr(exc, "code", None)
    message = (getattr(exc, "message", None) or str(exc) or "").lower()
    details = (getattr(exc, "details", None) or "").lower()
    hint = (getattr(exc, "hint", None) or "").lower()
    error_text = " ".join([message, details, hint])

    if code == "23505" or "duplicate key" in error_text or "unique constraint" in error_text:
        if "numerodocumento" in error_text or "documento" in error_text:
            return 409, "Este numero de documento ya esta registrado."
        if "correo" in error_text or "email" in error_text:
            return 409, "Este correo electronico ya esta registrado."
        return 409, "Ya existe un registro con esos datos."

    if code == "23503" or "foreign key" in error_text:
        return 409, "No se pudo completar la operacion porque falta un registro relacionado."

    if code == "23502" or "not-null" in error_text or "null value" in error_text:
        return 400, "Falta completar uno o mas campos obligatorios."

    if code == "23514" or "check constraint" in error_text:
        return 400, "Revisa los datos ingresados. Alguno no cumple las reglas del sistema."

    if "violates" in error_text or "constraint" in error_text:
        return 400, "No se pudo completar la operacion. Revisa los datos ingresados."

    return 500, "No se pudo procesar la solicitud. Intentalo nuevamente."


@app.exception_handler(APIError)
async def supabase_api_error_handler(request: Request, exc: APIError):
    status_code, detail = _friendly_database_error(exc)
    print(f"SUPABASE API ERROR: {type(exc).__name__}: {exc}")
    return JSONResponse(status_code=status_code, content={"detail": detail})


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print("GLOBAL EXCEPTION:")
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"detail": "Ocurrio un error inesperado. Intentalo nuevamente."},
    )


app.include_router(router)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "app": settings.app_name, "version": settings.app_version}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}
