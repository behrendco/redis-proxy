from collections import OrderedDict
from typing import Optional
import time

class LRUCache:
    def __init__(
            self, 
            capacity: int, 
            expiry_duration: int) -> None:
        """
        Initializes an LRUCache object.
        The cache is implemented using an OrderedDict object to track which 
        keys were least recently used.

        :param int capacity: Max capacity for the cache
        :param int expiry_duration: Time duration after which cache values will be expired

        :return: Returns nothing.
        :rtype: None
        """
        self.cache = OrderedDict()
        self.capacity = capacity
        self.expiry_duration = expiry_duration
    
    def get(
            self, 
            key: str) -> Optional[str]:
        """
        Gets the value associated with the passed key from the cache.

        :param str key: Key to check for in the cache.

        :return: Returns string value associated with the passed key if it exists, 
        else returns a null value.
        :rtype: Optional[str]
        """
        if key not in self.cache:
            return None
        
        value, expiry_time = self.cache[key]
        if time.time() > expiry_time:
            self.cache.pop(key)
            return None

        self.cache.move_to_end(key)
        return value
    
    def put(
            self, 
            key: str, 
            value: str) -> None:
        """
        Sets a value for its associated key in the cache.

        :param str key: String key name
        :param str value: String value data associated with key

        :return: Returns nothing.
        :rtype: None
        """
        expiry_time = time.time() + self.expiry_duration
        self.cache[key] = (value, expiry_time)
        self.cache.move_to_end(key)

        if len(self.cache) > self.capacity:
            self.cache.popitem(last = False)