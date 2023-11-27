from redis import Redis
from typing import Optional

class RedisClient:
    def __init__(
            self, 
            host: str, 
            port: int, 
            db: int) -> None:
        """
        Initializes a RedisClient object.

        :param str host: IP address/host name of the backing Redis
        :param int port: Port number of the backing Redis
        :param int db: Database of the backing Redis

        :return: Returns nothing.
        :rtype: None
        """
        self.redis = Redis(
            host = host, 
            port = port, 
            db = db, 
            decode_responses = True
        )

    def get(
            self, 
            key: str) -> Optional[str]:
        """
        Gets the value associated with the passed key from backing Redis.

        :param str key: Key to check for in the backing Redis.

        :return: Returns string value associated with the passed key if it exists, 
        else returns a null value.
        :rtype: Optional[str]
        """
        try:
            return self.redis.get(key)
        except:
            return None

    def put(
            self, 
            key: str, 
            value: str) -> Optional[bool]:
        """
        Sets a value for its associated key in the backing Redis.

        :param str key: String key name
        :param str value: String value data associated with key

        :return: Returns True if Redis SET command executed correctly, 
        otherwise returns a null value.
        :rtype: Optional[bool]
        """
        try:
            return self.redis.set(key, value)
        except:
            return None