from src.cache.cache import LRUCache
import time

class TestCache:
    def test_initialize(self):
        cache = LRUCache(5, 20)
        assert len(cache.cache) == 0

    def test_put(self):
        cache = LRUCache(5, 20)
        cache.put("a", "b")
        assert len(cache.cache) == 1

    def test_key_not_defined(self):
        cache = LRUCache(5, 20)
        value = cache.get("a")
        assert not value

    def test_key_defined(self):
        cache = LRUCache(5, 20)
        cache.put("a", "b")
        value = cache.get("a")
        assert value == "b"

    def test_expiry_time(self):
        cache = LRUCache(5, 2)
        cache.put("a", "b")
        time.sleep(3)
        value = cache.get("a")
        assert not value

    def test_lru_eviction_write(self):
        cache = LRUCache(5, 20)
        cache.put("a", "b")
        cache.put("c", "d")
        cache.put("e", "f")
        cache.put("g", "h")
        cache.put("i", "j")
        cache.put("k", "l")
        value = cache.get("a")
        assert len(cache.cache) == 5 and not value

    def test_lru_eviction_read(self):
        cache = LRUCache(5, 20)
        cache.put("a", "b")
        cache.put("c", "d")
        cache.put("e", "f")
        cache.put("g", "h")
        cache.put("i", "j")
        value = cache.get("a")
        cache.put("k", "l")
        value = cache.get("c")
        assert len(cache.cache) == 5 and not value