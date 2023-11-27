from redis import Redis
from src.config import Config
import socket
import threading

client_address = (Config.tcp_ip, Config.tcp_port)
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect(client_address)

redis = Redis(
    host = Config.redis_host, 
    port = Config.redis_port, 
    db = Config.redis_db, 
    decode_responses = True
)

class TestSocketServer:
    def send_command(
            host: str, 
            port: int, 
            command: str, 
            value: str) -> None:
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.connect((host, port))
        client_sock.send(command.encode())
        response = client_sock.recv(1032).decode()
        assert response == value
    
    def test_socket_server(self):
        pairs = [
            ("*2\r\n$3\r\nGET\r\n$1\r\nz\r\n", "_\r\n"), 
            ("*2\r\n$3\r\nGET\r\n$1\r\na\r\n", "$1\r\nb\r\n"), 
            ("*2\r\n$3\r\nget\r\n$1\r\nc\r\n", "$1\r\nd\r\n"), 
            ("*2\r\n$3\r\nGET\r\n$1\r\ne\r\n", "$1\r\nf\r\n"), 
            ("+OK\r\n", "-Invalid command\r\n"), 
            ("*3\r\n$3\r\nSET\r\n$1\r\na\r\n$1\r\nb\r\n", "-Only GET commands supported\r\n"), 
            ("*3\r\n$3\r\nGET\r\n$1\r\na\r\n$1\r\nb\r\n", "-Too many arguments\r\n")
        ]

        threads = []
        for command, value in pairs:
            client_thread = threading.Thread(
                target = TestSocketServer.send_command, 
                args = (Config.tcp_ip, Config.tcp_port, command, value)
            )
            threads.append(client_thread)
            client_thread.start()

        [thread.join() for thread in threads]