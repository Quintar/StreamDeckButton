import select
import socket
import threading
from streamcontroller_plugin_tools import BackendBase 
from loguru import logger as log


class Backend(BackendBase):
    HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
    PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
    max_clients = 2
    serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self):
        super().__init__()
        self.top_label : str = ""
        self.center_label : str = ""
        self.bottom_label : str = ""
        self.running = False
        log.info("Backend initialized")


    def start(self):
        log.info("Start server")
        if (not self.running):
            self.serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            threading.Thread(target=self._init_socket, args=(self.HOST, self.PORT,)).start()
        else: log.warning("Server still running")

    def _init_socket(self, host, port: int):
        log.info(f"Starting socket server on {host}:{port}")
        self.serv_socket.bind((host, port))
        self.serv_socket.listen(self.max_clients)
        while True:
            try:
                self.running = True
                client, address = self.serv_socket.accept()
                #log.info(f"Accepted connection from {address}")
                self._handle_client(client, address)
                #self.serv_socket.close() Socket close not neccesary?
            except Exception as e:
                log.warning(f"Error while establishing port {e}")
                self.running = False
                break

    def _handle_client(self, client, address):
        #log.info(f"Connection-Thread from {address}")
        try:
            request_bytes = b"" + client.recv(1024)
        except Exception as e:
            log.error(f"Error receiving data: {e}")
            client.close()
            return
        if not request_bytes:
            log.info("Connection closed")
            client.close()
            return
        client.close()
        request_str = request_bytes.decode(errors="ignore").strip()
        if("|" not in request_str): request_str += "|"
        result = request_str.split("|")
        if (result[0]): self.top_label = result[0]
        if (result[1]): self.center_label = result[1]
        if (result[2]): self.bottom_label = result[2]
        #log.info(request_str)
        self.frontend.trigger_event(
            event_id="com_quintar_streamdeckbutton::AdvancedEvent",
            data=result
        )

    def on_advanced_action_triggered(self, host, port):
        log.info(f"Restart server with new settings {host}:{port}")
        self.HOST = host
        self.PORT = port
        if(self.serv_socket):
            try:
                self.serv_socket.shutdown(0)
                self.serv_socket.close()
            except Exception as e:
                pass
        self.serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.inputs = [self.serv_socket]
        self.outputs = []
        self.start()

    def get_top_label(self) -> str:
        return self.top_label

    def get_center_label(self) -> str:
        return self.center_label

    def get_bottom_label(self) -> str:
        return self.bottom_label

backend = Backend()