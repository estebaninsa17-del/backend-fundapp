from supabase import Client


class CertificadoRepository:
    def __init__(self, client: Client):
        self._db = client

    def find_by_usuario(self, idusuarios: int) -> list[dict]:
        res = (
            self._db.schema("voluntariado").from_("certificados")
            .select("*")
            .eq("usuarios_idusuarios", idusuarios)
            .execute()
        )
        return res.data or []
