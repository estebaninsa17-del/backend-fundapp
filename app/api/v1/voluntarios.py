from fastapi import APIRouter

from app.core.dependencies import AdminUser, CurrentUser, get_user_id
from app.domain.schemas.voluntario import CreatePostulacionDTO, UpdateEstadoDTO
from app.infrastructure.repositories.voluntario_repository import VoluntarioRepository
from app.infrastructure.supabase_client import get_supabase_admin
from app.services.voluntario_service import VoluntarioService

router = APIRouter(prefix="/voluntarios", tags=["Voluntarios"])


def _service() -> VoluntarioService:
    return VoluntarioService(VoluntarioRepository(get_supabase_admin()))


@router.get("/postulaciones", summary="Listar postulaciones (Admin: todas | Voluntario: las suyas)")
def list_postulaciones(current_user: CurrentUser):
    svc = _service()
    if current_user.get("rol") == "admin":
        return svc.get_postulaciones(None)
    return svc.get_postulaciones(get_user_id(current_user))


@router.post("/postulaciones", status_code=201, summary="Postularse a una actividad")
def postular(dto: CreatePostulacionDTO, current_user: CurrentUser):
    return _service().postular(get_user_id(current_user), dto)


@router.patch("/postulaciones", summary="Actualizar estado de postulación [Admin]")
def update_estado(dto: UpdateEstadoDTO, admin: AdminUser):
    return _service().update_estado(dto.id, dto.estado)


@router.get("/", summary="Listar todos los voluntarios [Admin]")
def list_voluntarios(admin: AdminUser):
    return _service().get_all_voluntarios()
