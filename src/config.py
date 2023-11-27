import os

class Config:
    proxy_host = os.environ.get("PROXY_HOST")
    proxy_port = int(os.environ.get("PROXY_PORT"))
    cache_capacity = int(os.environ.get("CACHE_CAPACITY"))
    cache_expiry_duration = int(os.environ.get("CACHE_EXPIRY_DURATION"))
    redis_host = os.environ.get("REDIS_HOST")
    redis_port = int(os.environ.get("REDIS_PORT"))
    redis_db = int(os.environ.get("REDIS_DB"))
    tcp_ip = os.environ.get("TCP_IP")
    tcp_port = int(os.environ.get("TCP_PORT"))