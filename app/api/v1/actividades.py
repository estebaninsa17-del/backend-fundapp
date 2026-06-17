from fastapi import APIRouter

from app.core.dependencies import AdminUser
from app.domain.schemas.actividad import CreateActividadDTO, UpdateActividadDTO
from app.infrastructure.repositories.actividad_repository import ActividadRepository
from app.infrastructure.supabase_client import get_supabase_admin
from app.services.actividad_service import ActividadService

router = APIRouter(prefix="/actividades", tags=["Actividades"])


def _service() -> ActividadService:
    return ActividadService(ActividadRepository(get_supabase_admin()))


@router.get("/", summary="Listar todas las actividades (público)")
def list_actividades():
    return _service().get_all()


@router.get("/{idactividades}", summary="Obtener actividad por ID")
def get_actividad(idactividades: int):
    return _service().get_by_id(idactividades)


@router.post("/", status_code=201, summary="Crear actividad [Admin]")
def create_actividad(dto: CreateActividadDTO, admin: AdminUser):
    return _service().create(dto)


@router.patch("/{idactividades}", summary="Actualizar actividad [Admin]")
def update_actividad(idactividades: int, dto: UpdateActividadDTO, admin: AdminUser):
    return _service().update(idactividades, dto)


@router.delete("/{idactividades}", summary="Eliminar actividad [Admin]")
def delete_actividad(idactividades: int, admin: AdminUser):
    return _service().delete(idactividades)
