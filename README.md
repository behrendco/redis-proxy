# Redis Proxy

The Redis proxy is implemented as an HTTP web service using the Flask web framework and Gunicorn WSGI HTTP server. Additionally, an included TCP server allows clients to interface to the proxy through a subset of the Redis protocol.

## Architecture Overview

The proxy is used as a read-through cache, always first checking its LRU cache and returning the value from the cache in the case of a cache hit. In the case of a cache miss, the cache populates the missing data from the backing Redis, and returns it. If the value is not defined in the backing Redis, the proxy returns a null value.

### Redis

The backing Redis serves as an in-memory data structure store, storing string key-value pairs allowing values to be subsequently retrieved and manipulated, using the same key that was used to initially store them.

The address of the backing Redis is configurable at proxy startup in the `.env` file.

### LRU Cache

A GET request directed at the proxy returns the value from the proxy's local cache if the cache contains a value for that key. If it does not, the proxy fetches the value from the backing Redis instance.

The cache is implemented using an OrderedDict object to track which keys were least recently used, utilizing a doubly linked list to maintain the order of the elements under the hood.

Max capacity and global expiry duration values are also configurable in the `.env` file.

### HTTP Web Service

Multiple clients are able to concurrently connect to the proxy, with the configurable limit as well as host name and port defined in the `.env` file. API reference is below:

#### Health Check

Returns a message "Redis proxy service is up." to indicate the service is running.

```http
  GET /
```

#### Get Key Value

Utilizes the Redis proxy to check the cache and backing Redis for the value associated with the passed key parameter.

```http
  GET /get/${key}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `key`      | `string` | **Required**. Key of value to fetch |

### TCP Server

Clients can interface to the Redis proxy through a subset of the Redis protocol as opposed to using the HTTP protocol.

The server receives and decodes Redis commands from clients. It supports GET commands, accepting them as an array of bulk strings as noted in the [Redis serialization protocol (RESP) specification](https://redis.io/docs/reference/protocol-spec/#:~:text=Clients%20send%20commands%20to%20a%20Redis%20server%20as%20an%20array%20of%20bulk%20strings.). The server then encodes proper responses to the GET request as either a bulk string or nil value, noted [here](https://redis.io/commands/get/#:~:text=Return-,Bulk%20string%20reply,-%3A%20the%20value%20of), according to the RESP protocol and sends them back to the client.

Its host name and port are additionally configurable in the `.env` file.

## Code Structure

```
.
├── src
│   ├── app.py
│   ├── config.py
│   ├── socket_server.py
│   ├── cache
│   │   └── cache.py
│   │── client
│   │   └── client.py
│   │── proxy
│   │   └── proxy.py
│   └── resp
│       ├── decoder.py
│       └── encoder.py
├── tests
│   ├── test_http
│   │   ├── test_cache.py
│   │   ├── test_client.py
│   │   └── test_proxy.py
│   ├── test_tcp
│   │   ├── test_resp_decoder.py
│   │   ├── test_resp_encoder.py
│   │   └── test_socket_server.py
├── .env
├── docker-compose.yml
├── Dockerfile
├── Dockerfile-socket-server
├── Makefile
├── requirements.txt
└── README.md
```

## Algorithmic Complexity

The time complexity of cache get and put operations are constant, O(1). Space complexity is linear, O(n).

Additionally, Redis GET operations are O(1), as noted in the [Redis Documentation](https://redis.io/commands/get/#:~:text=Time%20complexity%3A,O(1)). So GET requests to the HTTP web service proxy are constant, while the TCP server requires linear time to encode/decode commands and responses in accordance with RESP.

## Run Proxy and Tests

To build the code and start the proxy and tests, use make with the following targets:

```
help: Show help for Makefile recipes.
build: Build or rebuild service.
run: Create and start containers.
stop: Stop and remove containers, networks.
test-flask: Execute HTTP web service tests.
test-socket-server: Execute Redis client protocol tests.
test: Build code and execute end-to-end tests.
restart: Stop, rebuild, restart containers.
```

This assumes the system has make, docker, docker-compose, and bash installed.

### Testing

After unpacking the code archive, enter the root project directory.

```bash
cd redis-proxy
```

Run end-to-end tests.

```bash
make test
```