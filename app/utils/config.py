import os
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from pathlib import Path
from typing import Tuple
from dotenv import load_dotenv

# .env yükle
BASE_DIR = Path(__file__).resolve().parents[2]
DOTENV_PATH = BASE_DIR / ".env"

if DOTENV_PATH.exists():
    load_dotenv(dotenv_path=DOTENV_PATH, override=True)

# === ENV HELPERS ===

def get_app_env() -> str:
    return os.getenv("APP_ENV", "dev").lower()

def is_dev() -> bool:
    return get_app_env() == "dev"


# === DATABASE ===

def _force_ssl(db_url: str) -> str:
    if not db_url:
        return db_url
    parsed = urlparse(db_url)
    qs = dict(parse_qsl(parsed.query, keep_blank_values=True))
    if "sslmode" not in qs:
        qs["sslmode"] = "require"
    new_query = urlencode(qs)
    return urlunparse(parsed._replace(query=new_query))

def get_database_url() -> str:
    """
    dev → LOCAL_DATABASE_URL yoksa DATABASE_URL fallback
    prod → DATABASE_URL zorunlu + sslmode=require
    """
    env = get_app_env()

    if env == "dev":
        db_url = (
            os.getenv("LOCAL_DATABASE_URL")
            or os.getenv("DATABASE_URL")
            or "postgresql://user:pass@localhost:5432/eiko"
        )
        return db_url

    # prod
    db_url = os.getenv("DATABASE_URL", "")
    if not db_url:
        raise RuntimeError("DATABASE_URL (prod) eksik.")
    return db_url


# === JWT ===

def get_jwt_settings() -> Tuple[str, str]:
    secret = os.getenv("JWT_SECRET_KEY", "")
    alg = os.getenv("JWT_ALGORITHM", "HS256")
    if not secret:
        raise RuntimeError("JWT_SECRET_KEY eksik.")
    return secret, alg


# === UVICORN ===

def get_uvicorn_bind() -> Tuple[str, int]:
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    return host, port

# === EXPORTS ===

APP_ENV = get_app_env()
DATABASE_URL = get_database_url()
JWT_SECRET_KEY, JWT_ALGORITHM = get_jwt_settings()