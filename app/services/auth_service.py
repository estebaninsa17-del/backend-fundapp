from fastapi import HTTPException, status

from app.core.security import create_access_token, hash_password, verify_password
from app.domain.schemas.auth import LoginDTO, RegisterDTO
from app.infrastructure.repositories.usuario_repository import UsuarioRepository


class AuthService:
    def __init__(self, repo: UsuarioRepository):
        self._repo = repo

    def login(self, dto: LoginDTO) -> dict:
        usuario = self._repo.find_by_email(dto.email)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas",
            )

        if not verify_password(dto.password, usuario["contrasena"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas",
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
                detail="El correo ya está registrado",
            )

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
