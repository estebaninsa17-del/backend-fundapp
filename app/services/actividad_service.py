from fastapi import HTTPException, status

from app.domain.schemas.actividad import CreateActividadDTO, UpdateActividadDTO
from app.infrastructure.repositories.actividad_repository import ActividadRepository


class ActividadService:
    def __init__(self, repo: ActividadRepository):
        self._repo = repo

    def get_all(self) -> list[dict]:
        return self._repo.find_all()

    def get_by_id(self, idactividades: int) -> dict:
        actividad = self._repo.find_by_id(idactividades)
        if not actividad:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Actividad no encontrada")
        return actividad

    def create(self, dto: CreateActividadDTO) -> dict:
        return self._repo.create(dto.model_dump(exclude_none=True))

    def update(self, idactividades: int, dto: UpdateActividadDTO) -> dict:
        self.get_by_id(idactividades)  # valida existencia
        data = dto.model_dump(exclude_none=True)
        if not data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sin datos para actualizar")
        return self._repo.update(idactividades, data)

    def delete(self, idactividades: int) -> dict:
        self.get_by_id(idactividades)
        self._repo.delete(idactividades)
        return {"message": "Actividad eliminada correctamente"}
