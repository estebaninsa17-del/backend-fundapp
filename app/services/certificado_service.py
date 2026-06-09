from app.infrastructure.repositories.certificado_repository import CertificadoRepository
from app.infrastructure.repositories.donacion_repository import DonacionRepository
from app.infrastructure.repositories.usuario_repository import UsuarioRepository


class CertificadoService:
    def __init__(
        self,
        cert_repo: CertificadoRepository,
        donacion_repo: DonacionRepository,
        usuario_repo: UsuarioRepository,
    ):
        self._certs = cert_repo
        self._donaciones = donacion_repo
        self._usuarios = usuario_repo

    def get_certificados_voluntario(self, idusuarios: int) -> list[dict]:
        return self._certs.find_by_usuario(idusuarios)

    def get_certificados_donacion(self, idusuarios: int) -> list[dict]:
        return self._donaciones.find_confirmed_by_usuario(idusuarios)

    def validar_por_documento(self, numerodocumento: int, tipodocumento: str) -> dict:
        from fastapi import HTTPException, status

        usuario = self._usuarios.find_by_documento(numerodocumento, tipodocumento)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado o inactivo",
            )

        certificados = self._certs.find_by_usuario(usuario["idusuarios"])
        donaciones = self._donaciones.find_confirmed_by_usuario(usuario["idusuarios"])
        usuario.pop("contrasena", None)

        return {"usuario": usuario, "certificados": certificados, "donaciones": donaciones}
