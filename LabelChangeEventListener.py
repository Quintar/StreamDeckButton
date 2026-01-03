import threading
import time
from loguru import logger as log
from src.backend.PluginManager.EventHolder import EventHolder


class LabelChangeEvent(EventHolder):

    def __init__(self, plugin_base: "PluginBase", event_id: str):
        super().__init__(plugin_base=plugin_base, event_id=event_id)
        log.info("Initializing LabelChangeEvent...")
