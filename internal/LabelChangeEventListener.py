import select
import socket
import threading
from loguru import logger as log
from src.backend.PluginManager.EventHolder import EventHolder

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

class LabelChangeEvent(EventHolder):
    max_clients = 1
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    inputs = [server_socket]
    outputs = []

    def __init__(self, plugin_base: "PluginBase", event_id: str):
        super().__init__(plugin_base=plugin_base, event_id=event_id)
        log.info("Initializing LabelChangeEvent...")
        self.server_thread = threading.Thread(target=self._start_loop)
        self.server_thread.daemon = True
        self.server_thread.start()

    def _start_loop(self):
        log.info("Starting server thread...")
        self._start_server()

    def _start_server(self): 
        try:
            self.server_socket.bind((HOST, PORT))
            self.server_socket.listen(self.max_clients)
            threading.Thread(target=self.init_socket).start()
            log.info("Server started successfully.")
        except Exception as e:
            log.error(f"Error starting server: {e}")

    def init_socket(self):
        log.info(f"Starting socket server on {HOST}:{PORT}")
        while True:
            readable, writable, exceptional = select.select(self.inputs, self.outputs, self.inputs, 1)
            for s in readable:
                if s is self.server_socket:
                    client, address = self.server_socket.accept()
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
        self.trigger_event(result)
        log.info(request_str)