import select
import socket
import threading
from streamcontroller_plugin_tools import BackendBase 
from loguru import logger as log

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
max_clients = 1
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(max_clients)
inputs = [server_socket]
outputs = []

class Backend(BackendBase):

    def __init__(self):
        super().__init__()
        self.top_label : str = ""
        self.center_label : str = ""
        self.bottom_label : str = ""
        threading.Thread(target=self.init_socket).start()                
        log.info("Backend initialized")

    def init_socket(self):
        log.info(f"Starting socket server on {HOST}:{PORT}")
        while True:
            readable, writable, exceptional = select.select(inputs, outputs, inputs, 1)
            for s in readable:
                if s is server_socket:
                    client, address = server_socket.accept()
                    log.info(f"Accepted connection from {address}")
                    threading.Thread(target=self.handle_client, args=(client, address)).start()
                else:
                    log.warning("Unknown socket readable")

    def handle_client(self, client, address):
        log.info(f"Connection-Thread from {address}")
        try:
            request_bytes = b"" + client.recv(1024)
        except Exception as e:
            log.error(f"Error receiving data: {e}")
            client.close()
            return
        if not request_bytes:
            log.info("Connection closed")
            client.close()
        request_str = request_bytes.decode(errors="ignore").strip()
        result = request_str.split("|")
        if (result[0]): self.top_label = result[0]
        if (result[1]): self.center_label = result[1]
        if (result[2]): self.bottom_label = result[2]
        log.info(request_str)

    def get_top_label(self) -> str:
        return self.top_label

    def get_center_label(self) -> str:
        return self.center_label

    def get_bottom_label(self) -> str:
        return self.bottom_label

backend = Backend()
