from os import SEEK_SET
import threading
import time
from loguru import logger as log

class ReadFileContinously():

    PATH = "lines.txt"
    COUNTDOWN = 1 #seconds
    frontend = {}

    def __init__(self, frontend):
        self.frontend = frontend
        self.top_label : str = ""
        self.center_label : str = ""
        self.bottom_label : str = ""
        self.running = False


    def start(self):
        if (not self.running):
            threading.Thread(target=self._init_file, args=(self.PATH,)).start()
        else: log.warning("Reader still running")

    def _init_file(self, path):
        try:
            while True:
                self.running = True
                # open file
                with open(self.PATH) as f:
                            # read file
                            line = f.readline()
                            self.handle_lines(line)
                            time.sleep(self.COUNTDOWN)
                    # close file (end of with)
        except Exception as e:
            self.running = False
            log.warning(f"Error while establishing port {e}")

    def handle_lines(self, line):
        request_str = line
        if("|" not in request_str): request_str += "|"
        result = request_str.split("|")
        if (len(result) >= 1): self.top_label = result[0]
        if (len(result) >= 2): self.center_label = result[1]
        if (len(result) >= 3): self.bottom_label = result[2]


    # get settings from frontend
    def set_path(self, path):
        self.PATH = path

    def set_interval(self, interval: float):
        self.COUNTDOWN = interval

    def get_top_label(self) -> str:
        return self.top_label

    def get_center_label(self) -> str:
        return self.center_label

    def get_bottom_label(self) -> str:
        return self.bottom_label