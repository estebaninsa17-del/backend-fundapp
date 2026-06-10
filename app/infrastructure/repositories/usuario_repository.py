from typing import Optional

from supabase import Client


def _first_or_none(data: list[dict] | None) -> Optional[dict]:
    return data[0] if data else None


class UsuarioRepository:
    def __init__(self, client: Client):
        self._db = client

    def find_by_email(self, correo: str) -> Optional[dict]:
        res = (
            self._db.schema("usuarios").from_("usuarios")
            .select("*")
            .eq("correo", correo)
            .limit(1)
            .execute()
        )
        return _first_or_none(res.data)

    def find_by_id(self, idusuarios: int) -> Optional[dict]:
        res = (
            self._db.schema("usuarios").from_("usuarios")
            .select("*")
            .eq("idusuarios", idusuarios)
            .limit(1)
            .execute()
        )
        return _first_or_none(res.data)

    def find_by_documento(self, numerodocumento: int, tipodocumento: str) -> Optional[dict]:
        res = (
            self._db.schema("usuarios").from_("usuarios")
            .select("*")
            .eq("numerodocumento", numerodocumento)
            .eq("tipodocumento", tipodocumento)
            .eq("estadodecuenta", "Activo")
            .limit(1)
            .execute()
        )
        return _first_or_none(res.data)

    def find_by_numero_documento(self, numerodocumento: int) -> Optional[dict]:
        res = (
            self._db.schema("usuarios").from_("usuarios")
            .select("*")
            .eq("numerodocumento", numerodocumento)
            .limit(1)
            .execute()
        )
        return _first_or_none(res.data)

    def create(self, data: dict) -> dict:
        res = (
            self._db.schema("usuarios").from_("usuarios")
            .insert(data)
            .execute()
        )
        inserted = _first_or_none(res.data)
        if not inserted and "correo" in data:
            inserted = self.find_by_email(data["correo"])
        return inserted or {}


    def get_role(self, idusuarios: int) -> str:
        """Retorna 'admin' o 'voluntario'."""
        res = (
            self._db.schema("usuarios").from_("roles_has_usuarios")
            .select("roles_idroles")
            .eq("usuarios_idusuarios", idusuarios)
            .limit(1)
            .execute()
        )
        role_link = _first_or_none(res.data)
        if not role_link:
            return "voluntario"

        role_res = (
            self._db.schema("usuarios").from_("roles")
            .select("nombrerol")
            .eq("idroles", role_link["roles_idroles"])
            .limit(1)
            .execute()
        )
        role = _first_or_none(role_res.data)
        if role and role["nombrerol"] == "Administrador General":
            return "admin"
        return "voluntario"

    def list_all(self) -> list[dict]:
        res = (
            self._db.schema("usuarios").from_("usuarios")
            .select("*")
            .execute()
        )
        return res.data or []
