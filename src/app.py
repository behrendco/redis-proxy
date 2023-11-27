from flask import Flask, jsonify
from proxy.proxy import RedisProxy
from config import Config

proxy = RedisProxy(
    capacity = Config.cache_capacity, 
    expiry_duration = Config.cache_expiry_duration, 
    host = Config.redis_host, 
    port = Config.redis_port, 
    db = Config.redis_db
)
 
app = Flask(__name__)
 
@app.route("/")
def up() -> str:
    """
    Health check route to ensure web service is running.

    :return: Returns a message to indicate the service is up.
    :rtype: str
    """
    return "Redis proxy service is up."

@app.route("/get/<key>")
def get(
    key: str) -> str:
    """
    Utilizes the Redis proxy to check the cache and backing Redis for 
    the value associated with the passed key parameter.

    :param str key: Key to check for in the data stores.

    :return: Returns value associated with key, or error message if key is not defined.
    :rtype: str
    """
    try:
        value = proxy.get(key)
        if not value:
            return jsonify({"error": f"Key {key} does not exist."})
    
        return jsonify({"key": key, "value": value})
    except Exception as e:
        return jsonify({"error": str(e)})
 
if __name__ == "__main__":
    app.run(host = Config.proxy_host, port = Config.proxy_port)