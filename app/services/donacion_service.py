from fastapi import HTTPException, status

from app.domain.schemas.donacion import CreateDonacionDTO
from app.infrastructure.repositories.donacion_repository import DonacionRepository
from app.infrastructure.repositories.usuario_repository import UsuarioRepository


class DonacionService:
    def __init__(self, donacion_repo: DonacionRepository, usuario_repo: UsuarioRepository):
        self._donaciones = donacion_repo
        self._usuarios = usuario_repo

    def get_all(self) -> list[dict]:
        return self._donaciones.find_all()

    def get_by_usuario(self, idusuarios: int) -> list[dict]:
        return self._donaciones.find_by_usuario(idusuarios)

    def create(self, dto: CreateDonacionDTO, idusuarios: int | None) -> dict:
        # Si no hay usuario autenticado, resolvemos o creamos uno invitado
        if idusuarios is None:
            if not dto.correo or not dto.nombrecompleto:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="nombre y correo son requeridos para donantes invitados",
                )
            existing = self._usuarios.find_by_email(str(dto.correo))
            if existing:
                idusuarios = existing["idusuarios"]
            else:
                import time
                new_user = self._usuarios.create(
                    {
                        "nombrecompleto": dto.nombrecompleto,
                        "numerodocumento": int(time.time()),
                        "tipodocumento": "CC",
                        "correo": str(dto.correo),
                        "contrasena": "invitado_sin_contrasena",
                        "estadodecuenta": "Activo",
                    }
                )
                idusuarios = new_user["idusuarios"]

        proposito = dto.propositodonacion or "Donación voluntaria general"
        donante = self._donaciones.create_donante(proposito, idusuarios)

        donacion = self._donaciones.create_donacion(
            {
                "monto": dto.monto,
                "metodopago": dto.metodopago.value,
                "anonima": "No",
                "estadopago": "Confirmada",
                "usuarios_idusuarios": idusuarios,
                "donante_idinvitados": donante["idinvitados"],
            }
        )
        return {"iddonaciones": donacion["iddonaciones"], "mensaje": "Donación procesada correctamente"}

    def get_stats(self) -> dict:
        return self._donaciones.get_stats()
