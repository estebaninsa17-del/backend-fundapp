from fastapi import APIRouter

from app.core.dependencies import AdminUser
from app.infrastructure.repositories.actividad_repository import ActividadRepository
from app.infrastructure.repositories.donacion_repository import DonacionRepository
from app.infrastructure.repositories.usuario_repository import UsuarioRepository
from app.infrastructure.repositories.voluntario_repository import VoluntarioRepository
from app.infrastructure.supabase_client import get_supabase_admin

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/stats", summary="Estadísticas generales del sistema [Admin]")
def get_stats(admin: AdminUser):
    db = get_supabase_admin()
    donacion_stats = DonacionRepository(db).get_stats()
    voluntarios = VoluntarioRepository(db).list_all()
    actividades = ActividadRepository(db).find_all()
    usuarios = UsuarioRepository(db).list_all()

    return {
        "usuarios_total": len(usuarios),
        "actividades_total": len(actividades),
        "voluntarios_total": len(voluntarios),
        **donacion_stats,
    }
