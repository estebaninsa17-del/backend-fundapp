from pydantic import BaseModel
from typing import Optional


class ActividadBase(BaseModel):
    nombreactividad: str
    descripcion: Optional[str] = None
    fechainicio: str
    fechafin: Optional[str] = None
    ubicaciones_idubicaciones: Optional[int] = None


class CreateActividadDTO(ActividadBase):
    pass


class UpdateActividadDTO(BaseModel):
    nombreactividad: Optional[str] = None
    descripcion: Optional[str] = None
    fechainicio: Optional[str] = None
    fechafin: Optional[str] = None
    ubicaciones_idubicaciones: Optional[int] = None


class ActividadResponse(ActividadBase):
    idactividades: int

    class Config:
        from_attributes = True
