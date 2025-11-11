from redis import Redis

from core.config import settings

redis = Redis(
    host=settings.redis.connection.host,
    port=settings.redis.connection.port,
    db=settings.redis.db.default,
    decode_responses=True,
)


def main() -> None:
    print(redis.ping())
    redis.set("name", "foo")
    print(redis.get("name"))
    redis.delete("name")
    print(redis.get("name"))
    print(redis.get("spam"))


if __name__ == "__main__":
    main()
