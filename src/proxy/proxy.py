from cache.cache import LRUCache
from client.client import RedisClient
from resp.decoder import RESPDecoder
from resp.encoder import RESPEncoder
from typing import Optional

class RedisProxy:
    def __init__(
            self, 
            capacity: int, 
            expiry_duration: int, 
            host: str, 
            port: int, 
            db: int, 
            use_RESP: bool = False) -> None:
        """
        Initializes a RedisProxy object.

        :param int capacity: Max capacity for the proxy's LRU cache
        :param int expiry_duration: Time duration after which cache values will be expired
        :param str host: IP address/host name of the backing Redis
        :param int port: Port number of the backing Redis
        :param int db: Database of the backing Redis
        :param bool use_RESP: Indicates whether clients connect through a subset of 
        the Redis protocol

        :return: Returns nothing.
        :rtype: None
        """
        self.cache = LRUCache(capacity, expiry_duration)
        self.redis = RedisClient(host, port, db)
        self.use_RESP = use_RESP

    def get(
            self, 
            key: str) -> Optional[str]:
        """
        Gets the value associated with the passed key.
        The proxy is used as a read-through cache, always first checking its 
        LRU cache and returning the value from the cache in the case of a cache hit.
        In the case of a cache miss, the cache populates the missing data from the 
        backing Redis, and returns it.
        If the value is not defined in the backing Redis, returns a null value.
        Note: The null data type represents non-existent values.
              Null's raw RESP encoding is _\r\n

        :param str key: Key to check for in the data stores

        :return: Returns string value associated with the passed key if it exists, 
        else returns a null value.
        :rtype: Optional[str]
        """
        cache_value = self.cache.get(key)
        if cache_value:
            if self.use_RESP:
                return RESPEncoder.encode_bulk_string(cache_value)
            return cache_value
        
        redis_value = self.redis.get(key)
        if redis_value:
            self.cache.put(key, redis_value)
            if self.use_RESP:
                return RESPEncoder.encode_bulk_string(redis_value)
            return redis_value
        
        if self.use_RESP:
            return "_\r\n"
        return None
    
    def put(
            self, 
            key: str, 
            value: str) -> None:
        """
        Sets a value for its associated key in the cache and backing Redis.

        :param str key: String key name
        :param str value: String value data associated with key

        :return: Returns nothing.
        :rtype: None
        """
        self.cache.put(key, value)
        self.redis.put(key, value)