from src.client.client import RedisClient
from src.config import Config

class TestClient:
    def test_put(self):
        redis = RedisClient(Config.redis_host, Config.redis_port, Config.redis_db)
        result = redis.put("a", "b")
        assert result

    def test_key_not_defined(self):
        redis = RedisClient(Config.redis_host, Config.redis_port, Config.redis_db)
        redis.redis.flushdb()
        value = redis.get("c")
        assert not value

    def test_key_defined(self):
        redis = RedisClient(Config.redis_host, Config.redis_port, Config.redis_db)
        redis.put("a", "b")
        value = redis.get("a")
        assert value == "b"