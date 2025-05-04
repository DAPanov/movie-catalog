import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
JSON_STORAGE_FILEPATH = BASE_DIR / "db.json"

LOG_LEVEL = logging.INFO
LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)


API_TOKENS: frozenset[str] = frozenset(
    {
        "L6keDgGDoxpcleNqis752g",
        "3_9p1uM0k3Ua5qWkdjOpiw",
    }
)
