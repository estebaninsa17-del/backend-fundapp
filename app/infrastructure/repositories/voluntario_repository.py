from typing import Optional

from supabase import Client


def _first_or_none(data: list[dict] | None) -> Optional[dict]:
    return data[0] if data else None


class VoluntarioRepository:
    def __init__(self, client: Client):
        self._db = client

    # ── Voluntarios ──────────────────────────────────────────────────────────

    def find_voluntario_by_usuario(self, idusuarios: int) -> Optional[dict]:
        res = (
            self._db.schema("voluntariado").from_("voluntarios")
            .select("idvoluntarios")
            .eq("usuarios_idusuarios", idusuarios)
            .limit(1)
            .execute()
        )
        return _first_or_none(res.data)

    def create_voluntario(self, idusuarios: int) -> dict:
        res = (
            self._db.schema("voluntariado").from_("voluntarios")
            .insert({"usuarios_idusuarios": idusuarios, "usuarios_idusuarios_ref": idusuarios})
            .execute()
        )
        return _first_or_none(res.data) or {}

    def list_all(self) -> list[dict]:
        res = (
            self._db.schema("voluntariado").from_("voluntarios")
            .select("*")
            .execute()
        )
        return res.data or []

    # ── Postulaciones ─────────────────────────────────────────────────────────

    def find_all_postulaciones(self) -> list[dict]:
        res = (
            self._db.schema("voluntariado").from_("postulaciones")
            .select("*")
            .execute()
        )
        return res.data or []

    def find_postulaciones_by_voluntario(self, idvoluntarios: int) -> list[dict]:
        res = (
            self._db.schema("voluntariado").from_("postulaciones")
            .select("*")
            .eq("voluntarios_idvoluntarios", idvoluntarios)
            .execute()
        )
        return res.data or []

    def find_postulacion_existente(self, idvoluntarios: int, idactividad: int) -> Optional[dict]:
        res = (
            self._db.schema("voluntariado").from_("postulaciones")
            .select("idpostulaciones")
            .eq("voluntarios_idvoluntarios", idvoluntarios)
            .eq("actividades_idactividades", idactividad)
            .limit(1)
            .execute()
        )
        return _first_or_none(res.data)

    def create_postulacion(self, data: dict) -> dict:
        res = (
            self._db.schema("voluntariado").from_("postulaciones")
            .insert(data)
            .execute()
        )
        return _first_or_none(res.data) or {}

    def update_estado(self, idpostulaciones: int, estadopostulacion: str) -> dict:
        res = (
            self._db.schema("voluntariado").from_("postulaciones")
            .update({"estadopostulacion": estadopostulacion})
            .eq("idpostulaciones", idpostulaciones)
            .execute()
        )
        return _first_or_none(res.data) or {}
