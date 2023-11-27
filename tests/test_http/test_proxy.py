from redis import Redis
from src.config import Config
import time
import requests

redis = Redis(
    host = Config.redis_host, 
    port = Config.redis_port, 
    db = Config.redis_db, 
    decode_responses = True
)

class TestProxy:
    def test_up(self):
        r = requests.get(f"http://{Config.proxy_host}:{Config.proxy_port}")
        assert r.text == "Redis proxy service is up."
    
    def test_key_not_defined(self):
        redis.flushdb()
        url = f"http://{Config.proxy_host}:{Config.proxy_port}/get/a"
        r = requests.get(url)
        r_json = r.json()
        assert "error" in r_json and r_json["error"] == "Key a does not exist."
    
    def test_key_defined(self):
        redis.set("a", "b")
        url = f"http://{Config.proxy_host}:{Config.proxy_port}/get/a"
        r = requests.get(url)
        r_json = r.json()
        assert "value" in r_json and r_json["value"] == "b"
    
    def test_same_key(self):
        redis.set("c", "d")
        url = f"http://{Config.proxy_host}:{Config.proxy_port}/get/c"
        r = requests.get(url)

        r = requests.get(url)
        r_json = r.json()
        assert "value" in r_json and r_json["value"] == "d"
    
    def test_cache_expiry_time(self):
        redis.set("e", "f")
        url = f"http://{Config.proxy_host}:{Config.proxy_port}/get/e"
        r = requests.get(url)

        time.sleep(Config.cache_expiry_duration + 1)
        r = requests.get(url)
        r_json = r.json()
        assert "value" in r_json and r_json["value"] == "f"

    def test_cache_capacity(self):
        pairs = [("a", "b"), ("c", "d"), ("e", "f"), ("g", "h"), ("i", "j")]
        for key, value in pairs:
            redis.set(key, value)
            url = f"http://{Config.proxy_host}:{Config.proxy_port}/get/" + key
            r = requests.get(url)

        redis.set("k", "l")
        url = f"http://{Config.proxy_host}:{Config.proxy_port}/get/k"
        r = requests.get(url)
        r_json = r.json()
        assert "value" in r_json and r_json["value"] == "l"