from fastapi import HTTPException, status
from postgrest.exceptions import APIError

from app.core.security import create_access_token, hash_password, verify_password
from app.domain.schemas.auth import LoginDTO, RegisterDTO
from app.infrastructure.repositories.usuario_repository import UsuarioRepository


def _is_duplicate_document_error(exc: Exception) -> bool:
    error_text = str(exc).lower()
    return (
        "usuarios_numerodocumento_key" in error_text
        or ("duplicate key" in error_text and "documento" in error_text)
        or ("unique constraint" in error_text and "documento" in error_text)
    )


def _is_duplicate_email_error(exc: Exception) -> bool:
    error_text = str(exc).lower()
    return (
        "usuarios_correo_key" in error_text
        or ("duplicate key" in error_text and ("correo" in error_text or "email" in error_text))
        or ("unique constraint" in error_text and ("correo" in error_text or "email" in error_text))
    )


class AuthService:
    def __init__(self, repo: UsuarioRepository):
        self._repo = repo

    def login(self, dto: LoginDTO) -> dict:
        usuario = self._repo.find_by_email(dto.email)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales invalidas",
            )

        if not verify_password(dto.password, usuario["contrasena"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales invalidas",
            )

        rol = self._repo.get_role(usuario["idusuarios"])
        usuario.pop("contrasena", None)
        user_data = {**usuario, "rol": rol, "esAdmin": rol == "admin"}

        token = create_access_token(
            {
                "id": usuario["idusuarios"],
                "idusuarios": usuario["idusuarios"],
                "rol": rol,
                "esAdmin": rol == "admin",
            }
        )
        return {"user": user_data, "token": token}

    def register(self, dto: RegisterDTO) -> dict:
        existing = self._repo.find_by_email(dto.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Este correo electronico ya esta registrado.",
            )

        existing_document = self._repo.find_by_numero_documento(int(dto.numerodocumento))
        if existing_document:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Este numero de documento ya esta registrado.",
            )

        try:
            new_user = self._repo.create(
                {
                    "nombrecompleto": dto.nombrecompleto,
                    "numerodocumento": int(dto.numerodocumento),
                    "tipodocumento": dto.tipodocumento,
                    "correo": dto.email,
                    "contrasena": hash_password(dto.password),
                    "estadodecuenta": "Activo",
                }
            )
        except APIError as exc:
            if _is_duplicate_document_error(exc):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Este numero de documento ya esta registrado.",
                ) from exc
            if _is_duplicate_email_error(exc):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Este correo electronico ya esta registrado.",
                ) from exc
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se pudo registrar el usuario. Revisa los datos e intentalo nuevamente.",
            ) from exc

        if not new_user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No se pudo registrar el usuario. Revisa los datos e intentalo nuevamente.",
            )

        new_user.pop("contrasena", None)
        user_data = {**new_user, "rol": "voluntario", "esAdmin": False}
        token = create_access_token(
            {
                "id": new_user["idusuarios"],
                "idusuarios": new_user["idusuarios"],
                "rol": "voluntario",
                "esAdmin": False,
            }
        )
        return {"user": user_data, "token": token}
