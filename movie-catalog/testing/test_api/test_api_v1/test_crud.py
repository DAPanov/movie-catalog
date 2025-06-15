from os import getenv

if getenv("TESTING") != "1":
    raise OSError("Environment is not ready for testing")  # noqa: TRY003, EM101
