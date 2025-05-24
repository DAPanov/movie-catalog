from redis import Redis

from core import config

redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB,
    decode_responses=True,
)


def main() -> None:
    print(redis.ping())
    redis.set("name", "foo")
    print(redis.get("name"))
    redis.delete("name")
    print(redis.get("name"))


if __name__ == "__main__":
    main()
