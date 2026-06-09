from fastapi import APIRouter

from app.core.dependencies import CurrentUser, OptionalUser, get_user_id
from app.domain.schemas.donacion import CreateDonacionDTO
from app.infrastructure.repositories.donacion_repository import DonacionRepository
from app.infrastructure.repositories.usuario_repository import UsuarioRepository
from app.infrastructure.supabase_client import get_supabase_admin
from app.services.donacion_service import DonacionService

router = APIRouter(prefix="/donaciones", tags=["Donaciones"])


def _service() -> DonacionService:
    db = get_supabase_admin()
    return DonacionService(DonacionRepository(db), UsuarioRepository(db))


@router.get("/", summary="Listar donaciones (Admin: todas | Voluntario: las suyas)")
def list_donaciones(current_user: CurrentUser):
    svc = _service()
    if current_user.get("rol") == "admin":
        return svc.get_all()
    return svc.get_by_usuario(get_user_id(current_user))


@router.post("/", status_code=201, summary="Registrar donación (autenticado o invitado)")
def create_donacion(dto: CreateDonacionDTO, user: OptionalUser):
    idusuarios = get_user_id(user) if user else None
    return _service().create(dto, idusuarios)
