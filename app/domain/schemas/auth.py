from pydantic import BaseModel, EmailStr, field_validator


class LoginDTO(BaseModel):
    email: EmailStr
    password: str


class RegisterDTO(BaseModel):
    nombrecompleto: str
    numerodocumento: str
    tipodocumento: str = "CC"
    email: EmailStr
    password: str

    @field_validator("numerodocumento")
    @classmethod
    def documento_numerico(cls, value: str) -> str:
        if not value.isdigit():
            raise ValueError("El numero de documento debe contener solo digitos")
        return value


class TokenResponse(BaseModel):
    token: str
    user: dict
