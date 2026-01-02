# Import StreamController modules
from src.backend.PluginManager.ActionBase import ActionBase
from src.backend.DeckManagement.DeckController import DeckController
from src.backend.PageManagement.Page import Page
from src.backend.PluginManager.PluginBase import PluginBase
from loguru import logger as log


# Import python modules
import os

# Import gtk modules - used for the config rows
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

class DisplayAction(ActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plugin_base.connect_to_event(event_id="com_quintar_streamdeckbutton::LabelChangeEvent",
                                          callback=self.on_label_change)
                
    def on_ready(self) -> None:
        log.info("StreamDeck Button Plugin is ready!")
        icon_path = os.path.join(self.plugin_base.PATH, "assets", "info.png")
        self.set_media(media_path=icon_path, size=0.75)        
        
    def on_key_down(self) -> None:
        pass
    
    def on_key_up(self) -> None:
        pass

    async def on_label_change(self, *args, **kwargs):
        log.info(f"Label change event received with args: {args}")
        eventName = ""
        labels = []
        if(len(args) >= 2):
            eventName = str(args[0])
            labels = args[1]

        if(len(labels) >= 1): self.set_top_label   (str(labels[0]))
        if(len(labels) >= 2): self.set_center_label(str(labels[1]))
        if(len(labels) >= 3): self.set_bottom_label(str(labels[2]))