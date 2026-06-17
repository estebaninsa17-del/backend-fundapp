from pydantic import BaseModel
from typing import Optional


class CertificadoResponse(BaseModel):
    idcertificados: int
    nombrevoluntario: str
    actividadasociada: str
    actividades_idactividades: Optional[int]
    usuarios_idusuarios: Optional[int]

    class Config:
        from_attributes = True


class ValidarCertificadoDTO(BaseModel):
    numerodocumento: int
    tipodocumento: str
