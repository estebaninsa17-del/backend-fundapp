from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from enum import Enum


class MetodoPago(str, Enum):
    efectivo = "Efectivo"
    transferencia = "Transferencia"
    tarjeta_debito = "Tarjeta Débito"
    tarjeta_credito = "Tarjeta Crédito"
    pse = "PSE"
    nequi = "Nequi"
    daviplata = "Daviplata"


class EstadoPago(str, Enum):
    pendiente = "Pendiente"
    confirmada = "Confirmada"
    rechazada = "Rechazada"
    anulada = "Anulada"


class CreateDonacionDTO(BaseModel):
    monto: float
    metodopago: MetodoPago
    propositodonacion: Optional[str] = "Donación voluntaria general"
    # Solo requeridos si el donante no está autenticado
    nombrecompleto: Optional[str] = None
    correo: Optional[EmailStr] = None

    @field_validator("monto")
    @classmethod
    def monto_positivo(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("El monto debe ser mayor a 0")
        return v


class DonacionResponse(BaseModel):
    iddonaciones: int
    fechadonacion: Optional[str]
    monto: float
    estadopago: str
    metodopago: str
    usuarios_idusuarios: Optional[int]
    anonima: str

    class Config:
        from_attributes = True
