from functools import lru_cache

from supabase import Client, create_client

from app.core.config import get_settings


def _normalize_supabase_url(url: str) -> str:
    """Acepta la URL del proyecto aunque venga pegada con /rest/v1."""
    clean_url = url.strip().rstrip("/")
    if clean_url.endswith("/rest/v1"):
        clean_url = clean_url[: -len("/rest/v1")]
    return clean_url


@lru_cache()
def get_supabase() -> Client:
    """Retorna un cliente Supabase singleton (anon key)."""
    s = get_settings()
    return create_client(_normalize_supabase_url(s.supabase_url), s.supabase_key)


@lru_cache()
def get_supabase_admin() -> Client:
    """Retorna un cliente Supabase con service role key (operaciones admin)."""
    s = get_settings()
    key = s.supabase_service_key or s.supabase_key
    return create_client(_normalize_supabase_url(s.supabase_url), key)
