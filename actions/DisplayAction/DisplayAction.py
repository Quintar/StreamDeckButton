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
                
    def on_ready(self) -> None:
        log.info("StreamDeck Button Plugin is ready!")
        icon_path = os.path.join(self.plugin_base.PATH, "assets", "info.png")
        self.set_media(media_path=icon_path, size=0.75)        
        
    def on_key_down(self) -> None:
        self.set_center_label(str("Pressed"))
        log.info("Key down")
    
    def on_key_up(self) -> None:
        self.set_center_label(str("Released"))
        log.info("Key up")

    def on_tick(self) -> None:
        if(self.plugin_base.backend): 
            self.set_top_label   (str(self.plugin_base.backend.get_top_label()))
            self.set_center_label(str(self.plugin_base.backend.get_center_label()))
            self.set_bottom_label(str(self.plugin_base.backend.get_bottom_label()))
        # This function is called every second if a tick interval is set in the action's settings
        pass