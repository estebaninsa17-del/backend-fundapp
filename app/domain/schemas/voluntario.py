from pydantic import BaseModel
from typing import Optional


class CreatePostulacionDTO(BaseModel):
    actividades_idactividades: int


class UpdateEstadoDTO(BaseModel):
    id: int
    estado: str


class PostulacionResponse(BaseModel):
    idpostulaciones: int
    fechapostulacion: Optional[str]
    estadopostulacion: str
    voluntarios_idvoluntarios: int
    actividades_idactividades: int
    comentario: Optional[str] = None

    class Config:
        from_attributes = True
