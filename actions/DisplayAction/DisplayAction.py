# Import StreamController modules
import random

from ...settings_file import KEY_CHECK_INTERVAL, KEY_FILE_PATH
from .read_file_continously import ReadFileContinously
from src.backend.PluginManager.ActionBase import ActionBase
from src.backend.DeckManagement.DeckController import DeckController
from src.backend.PageManagement.Page import Page
from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.PluginManager.EventHolder import EventHolder
from src.backend.PluginManager.EventAssigner import EventAssigner
from src.backend.PluginManager.InputBases import Input
from loguru import logger as log
from typing import Any, List

# Import python modules
import os

# Import gtk modules - used for the config rows
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

class DisplayAction(ActionBase):
    ready = False
    file_reader = {}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.plugin_base.asset_manager.icons.add_listener(self._icon_changed)
        self.plugin_base.asset_manager.colors.add_listener(self._color_changed)

        self.plugin_base.connect_to_event(
            event_id="com_quintar_streamdeckbutton::DataReceiveEvent",
            callback=self.on_label_change
        )

        self.plugin_base.connect_to_event(
            event_id="com_quintar_streamdeckbutton::SettingsChangedEvent",
            callback=self.on_settings_change
        )

                
    def on_ready(self) -> None:
        log.info("StreamDeck Button Plugin is ready!")
        
        icon_path = os.path.join(self.plugin_base.PATH, "assets", "info.png")
        self.set_media(media_path=icon_path, size=0.75)
        self.file_reader = ReadFileContinously(self.plugin_base)
        settings = self.plugin_base.get_settings()
        self._set_file_reader_settings(settings.get(KEY_FILE_PATH, ""), settings.get(KEY_CHECK_INTERVAL, "1.0"))
        self.file_reader.start()
        ready = True
        
    def on_key_down(self) -> None:
        pass
    
    def on_key_up(self) -> None:
        #self.display_settings()
        self.file_reader.start()

    async def _icon_changed(self, event: str, key: str, asset: Any) -> None:
        if not key in self.icon_keys:
            return
        if key != self.icon_name:
            return
        self.current_icon = asset
        self.icon_name = key
        self.display_icon()

    def display_color(self) -> None:
        if not self.current_color:
            return
        color = self.current_color.get_values()
        try:
            self.set_background_color(color)
        except:
            # Sometimes we try to call this too early, and it leads to
            # console errors, but no real errors. Ignoring this for now
            pass

    async def _color_changed(self, event: str, key: str, asset: Any) -> None:
        if not key in self.color_keys:
            return
        if key != self.color_name:
            return
        self.current_color = asset
        self.color_name = key
        self.display_color()

    def display_settings(self):
        settings = self.get_settings()
#        self.plugin_base.backend.set_path(self.ip_row.get_text(), int(self.port_row.get_text()))
        log.info(f"Current Settings: {settings}")
        #self.set_top_label      (settings["file_path"])
#        self.set_center_label   (self.port_row.get_text())


    def on_label_change(self, *args, **kwargs):
        #log.info(f"Label change event received with args: {args} {kwargs}")
        eventName = ""
        labels = []
        if(len(kwargs) >= 2):
            eventName = str(args[0])
            labels = kwargs["data"]

        if(len(labels) >= 1): self.set_top_label   (str(labels[0]))
        if(len(labels) >= 2): self.set_center_label(str(labels[1]))
        if(len(labels) >= 3): self.set_bottom_label(str(labels[2]))

    def on_tick(self):
        self.set_top_label   (str(self.file_reader.top_label))
        self.set_center_label(str(self.file_reader.center_label))
        self.set_bottom_label(str(self.file_reader.bottom_label))


    def on_settings_change(self, *args, **kwargs):
        log.info(f"Args: {kwargs}")
        self._set_file_reader_settings(kwargs["data"][0], kwargs["data"][1])
        
    def _set_file_reader_settings(self, file_path, interval):
        self.file_reader.set_path(file_path)
        self.file_reader.set_interval(interval)
