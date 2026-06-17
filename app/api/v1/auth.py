from fastapi import APIRouter

from app.core.dependencies import CurrentUser
from app.domain.schemas.auth import LoginDTO, RegisterDTO, TokenResponse
from app.infrastructure.repositories.usuario_repository import UsuarioRepository
from app.infrastructure.supabase_client import get_supabase_admin
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


def _service() -> AuthService:
    return AuthService(UsuarioRepository(get_supabase_admin()))


@router.post("/login", response_model=TokenResponse, summary="Iniciar sesion")
def login(dto: LoginDTO):
    return _service().login(dto)


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=201,
    summary="Registrar nuevo usuario",
)
def register(dto: RegisterDTO):
    return _service().register(dto)


@router.get("/me", summary="Obtener usuario autenticado")
def me(current_user: CurrentUser):
    """Retorna los datos del token JWT actual."""
    return current_user
