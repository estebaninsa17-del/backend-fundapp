from fastapi import HTTPException, status

from app.domain.schemas.voluntario import CreatePostulacionDTO
from app.infrastructure.repositories.voluntario_repository import VoluntarioRepository


class VoluntarioService:
    def __init__(self, repo: VoluntarioRepository):
        self._repo = repo

    def get_postulaciones(self, idusuarios: int | None) -> list[dict]:
        if idusuarios is None:
            return self._repo.find_all_postulaciones()

        voluntario = self._repo.find_voluntario_by_usuario(idusuarios)
        if not voluntario:
            return []
        return self._repo.find_postulaciones_by_voluntario(voluntario["idvoluntarios"])

    def postular(self, idusuarios: int, dto: CreatePostulacionDTO) -> dict:
        # Busca o crea el registro de voluntario
        voluntario = self._repo.find_voluntario_by_usuario(idusuarios)
        if not voluntario:
            voluntario = self._repo.create_voluntario(idusuarios)

        # Evita duplicados
        existing = self._repo.find_postulacion_existente(
            voluntario["idvoluntarios"], dto.actividades_idactividades
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya estás postulado a esta actividad",
            )

        return self._repo.create_postulacion(
            {
                "voluntarios_idvoluntarios": voluntario["idvoluntarios"],
                "voluntarios_usuarios_idusuarios": idusuarios,
                "usuarios_idusuarios": idusuarios,
                "actividades_idactividades": dto.actividades_idactividades,
                "estadopostulacion": "Pendiente",
                "comentario": None,
            }
        )

    def update_estado(self, idpostulaciones: int, estadopostulacion: str) -> dict:
        estados_validos = ["Pendiente", "Aprobado", "Rechazado", "Completado"]
        if estadopostulacion not in estados_validos:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Estado inválido. Valores permitidos: {estados_validos}",
            )
        postulacion = self._repo.update_estado(idpostulaciones, estadopostulacion)
        if not postulacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Postulación no encontrada",
            )
        return postulacion

    def get_all_voluntarios(self) -> list[dict]:
        return self._repo.list_all()
