from typing import Optional

from supabase import Client


def _first_or_none(data: list[dict] | None) -> Optional[dict]:
    return data[0] if data else None


class ActividadRepository:
    def __init__(self, client: Client):
        self._db = client

    def find_all(self) -> list[dict]:
        res = (
            self._db.schema("voluntariado").from_("actividades")
            .select("*")
            .order("fechainicio", desc=True)
            .execute()
        )
        return res.data or []

    def find_by_id(self, idactividades: int) -> Optional[dict]:
        res = (
            self._db.schema("voluntariado").from_("actividades")
            .select("*")
            .eq("idactividades", idactividades)
            .limit(1)
            .execute()
        )
        return _first_or_none(res.data)

    def create(self, data: dict) -> dict:
        res = (
            self._db.schema("voluntariado").from_("actividades")
            .insert(data)
            .execute()
        )
        return _first_or_none(res.data) or {}

    def update(self, idactividades: int, data: dict) -> dict:
        res = (
            self._db.schema("voluntariado").from_("actividades")
            .update(data)
            .eq("idactividades", idactividades)
            .execute()
        )
        return _first_or_none(res.data) or {}

    def delete(self, idactividades: int) -> bool:
        self._db.schema("voluntariado").from_("actividades").delete().eq(
            "idactividades", idactividades
        ).execute()
        return True
