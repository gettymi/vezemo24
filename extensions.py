"""Розширення Flask, винесені окремо — щоб уникнути циклічних імпортів."""
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect

from config import Config

csrf = CSRFProtect()

# Сховище: Redis, якщо налаштований, інакше памʼять процесу.
# Раніше ліміт мовчки не працював взагалі — REDIS_URL не існував у конфізі.
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[],
    storage_uri=Config.REDIS_URL or "memory://",
    strategy="fixed-window",
)
