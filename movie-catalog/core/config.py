import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
JSON_STORAGE_FILEPATH = BASE_DIR / "db.json"

LOG_LEVEL = logging.INFO
LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)


REDIS_HOST: str = "localhost"
REDIS_PORT: int = 6379
REDIS_DB: int = 0
REDIS_DB_TOKENS: int = 1
REDIS_DB_USERS: int = 2


REDIS_SET_TOKENS_NAME: str = "tokens"
