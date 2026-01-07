import threading
import time
from streamcontroller_plugin_tools import BackendBase 
from loguru import logger as log

class Backend(BackendBase):

    PATH = "lines.txt"
    COUNTDOWN = 1 #seconds

    def __init__(self):
        super().__init__()
        self.top_label : str = ""
        self.center_label : str = ""
        self.bottom_label : str = ""
        self.running = False
        log.info("Backend initialized")


    def start(self):
        log.info("Start reader")
        if (not self.running):
            #self.serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            threading.Thread(target=self._init_file, args=(self.PATH,)).start()
        else: log.warning("Reader still running")

    def _init_file(self, path):
        log.info(f"Starting reader server on {path}")
        while True:
            try:
                self.running = True
                # open file
                with open(self.PATH) as f:
                    # read file
                    line = f.readline()
                    self.handle_lines(line)
                    time.sleep(self.COUNTDOWN)
                # close file (end of with)
                #f.close()
            except Exception as e:
                self.running = False
                log.warning(f"Error while establishing port {e}")
                break

    def handle_lines(self, line):
        request_str = line #.decode(errors="ignore").strip()
        if("|" not in request_str): request_str += "|"
        result = request_str.split("|")
        if (len(result) >= 1): self.top_label = result[0]
        if (len(result) >= 2): self.center_label = result[1]
        if (len(result) >= 3): self.bottom_label = result[2]
        #log.info(request_str)
        self.frontend.trigger_event(
            event_id="com_quintar_streamdeckbutton::AdvancedEvent",
            data=result
        )


    # get settings from frontend
    def set_path(self, path):
        log.info(f"Restart reader with new settings {path}")
        self.PATH = path

    def set_interval(self, interval: float):
        self.COUNTDOWN = interval

    def get_top_label(self) -> str:
        return self.top_label

    def get_center_label(self) -> str:
        return self.center_label

    def get_bottom_label(self) -> str:
        return self.bottom_label

backend = Backend()