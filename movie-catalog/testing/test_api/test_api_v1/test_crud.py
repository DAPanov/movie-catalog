from os import getenv

from core.config import TEST_ENVIRONMENT_MSG_ERROR

if getenv("TESTING") != "1":
    raise OSError(TEST_ENVIRONMENT_MSG_ERROR)
