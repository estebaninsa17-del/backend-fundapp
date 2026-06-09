from fastapi import APIRouter

from app.core.dependencies import CurrentUser, get_user_id
from app.domain.schemas.certificado import ValidarCertificadoDTO
from app.infrastructure.repositories.certificado_repository import CertificadoRepository
from app.infrastructure.repositories.donacion_repository import DonacionRepository
from app.infrastructure.repositories.usuario_repository import UsuarioRepository
from app.infrastructure.supabase_client import get_supabase_admin
from app.services.certificado_service import CertificadoService

router = APIRouter(prefix="/certificados", tags=["Certificados"])


def _service() -> CertificadoService:
    db = get_supabase_admin()
    return CertificadoService(CertificadoRepository(db), DonacionRepository(db), UsuarioRepository(db))


@router.get("/voluntariado", summary="Mis certificados de voluntariado")
def mis_certificados_voluntariado(current_user: CurrentUser):
    return _service().get_certificados_voluntario(get_user_id(current_user))


@router.get("/donaciones", summary="Mis certificados de donaciones")
def mis_certificados_donacion(current_user: CurrentUser):
    return _service().get_certificados_donacion(get_user_id(current_user))


@router.post("/validar", summary="Validar certificados por documento (público)")
def validar_certificados(dto: ValidarCertificadoDTO):
    return _service().validar_por_documento(dto.numerodocumento, dto.tipodocumento)
