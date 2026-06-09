from typing import Optional

from supabase import Client


class DonacionRepository:
    def __init__(self, client: Client):
        self._db = client

    def find_all(self) -> list[dict]:
        res = (
            self._db.schema("donaciones").from_("donaciones")
            .select("*")
            .order("fechadonacion", desc=True)
            .execute()
        )
        return res.data or []

    def find_by_usuario(self, idusuarios: int) -> list[dict]:
        res = (
            self._db.schema("donaciones").from_("donaciones")
            .select("*")
            .eq("usuarios_idusuarios", idusuarios)
            .order("fechadonacion", desc=True)
            .execute()
        )
        return res.data or []

    def find_confirmed_by_usuario(self, idusuarios: int) -> list[dict]:
        res = (
            self._db.schema("donaciones").from_("donaciones")
            .select("*")
            .eq("usuarios_idusuarios", idusuarios)
            .eq("estadopago", "Confirmada")
            .execute()
        )
        return res.data or []

    def create_donante(self, proposito: str, idusuarios: int) -> dict:
        res = (
            self._db.schema("donaciones").from_("donante")
            .insert({"propositodonacion": proposito, "usuarios_idusuarios": idusuarios})
            .execute()
        )
        return (res.data or [None])[0] or {}

    def create_donacion(self, data: dict) -> dict:
        res = (
            self._db.schema("donaciones").from_("donaciones")
            .insert(data)
            .execute()
        )
        return (res.data or [None])[0] or {}

    def get_stats(self) -> dict:
        res = self._db.schema("donaciones").from_("donaciones").select("monto, estadopago").execute()
        donaciones = res.data or []
        total = sum(d["monto"] for d in donaciones if d["estadopago"] == "Confirmada")
        return {
            "total_donaciones": len(donaciones),
            "monto_total": total,
            "confirmadas": sum(1 for d in donaciones if d["estadopago"] == "Confirmada"),
        }
