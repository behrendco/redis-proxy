from proxy.proxy import RedisProxy
from resp.decoder import RESPDecoder
from resp.encoder import RESPEncoder
from config import Config
import socket
import multiprocessing

proxy = RedisProxy(
    capacity = Config.cache_capacity, 
    expiry_duration = Config.cache_expiry_duration, 
    host = Config.redis_host, 
    port = Config.redis_port, 
    db = Config.redis_db, 
    use_RESP = True
)

class Server:
    def __init__(
            self, 
            host: str, 
            port: int) -> None:
        """
        Initializes a Server object.

        :param str host: Server host IP address
        :param int port: Server port number

        :return: Returns nothing.
        :rtype: None
        """
        self.host = host
        self.port = port

    def handle(
            connection, 
            address) -> None:
        """
        Receives and decodes Redis commands from clients.
        The server supports GET commands as an array of bulk strings.
        Encodes proper responses according to the Redis serialization protocol (RESP) 
        and sends them back to the client.

        :param conenction: Socket object used to send and receive data on the connection
        :param address: Client address bound to the socket

        :return: Returns nothing. Closes connection after processing.
        :rtype: None
        """
        try:
            command = connection.recv(1024).decode()
            command = RESPDecoder.decode_command(command)

            if command[0] == "Invalid command":
                connection.send(RESPEncoder.encode_error("Invalid command").encode())
            elif command[0].upper() != "GET":
                connection.send(RESPEncoder.encode_error("Only GET commands supported").encode())
            elif len(command) > 2:
                connection.send(RESPEncoder.encode_error("Too many arguments").encode())
            else:
                key = command[1]
                value = proxy.get(key)
                connection.send(value.encode())
        finally:
            connection.close()

    def start(
            self) -> None:
        """
        Binds Server object to its host and listens for connections.

        :return: Returns nothing. Sets up processes to handle connections from clients.
        :rtype: None
        """
        address = (self.host, self.port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(address)
        self.sock.listen(1)

        while True:
            connection, client_address = self.sock.accept()
            process = multiprocessing.Process(
                target = Server.handle, args = (connection, client_address)
            )
            process.daemon = True
            process.start()

if __name__ == "__main__":
    server = Server(Config.tcp_ip, Config.tcp_port)
    try:
        server.start()
    finally:
        for process in multiprocessing.active_children():
            process.terminate()
            process.join()