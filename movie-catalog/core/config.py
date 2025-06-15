import logging
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

LOG_LEVEL = logging.INFO
LOG_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)


REDIS_HOST = "localhost"
REDIS_PORT = os.getenv("REDIS_PORT", "0") or 6379
REDIS_DB = 0
REDIS_DB_TOKENS = 1
REDIS_DB_USERS = 2
REDIS_DB_MOVIES_CATALOG = 3


REDIS_SET_TOKENS_NAME = "tokens"
REDIS_HASH_MOVIES_CATALOG_NAME = "movies-catalog"

TEST_ENVIRONMENT_MSG_ERROR = "Environment is not ready for testing"
