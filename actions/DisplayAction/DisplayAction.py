# Import StreamController modules
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
from gi.repository import Gtk, Adw
from GtkHelper.GenerativeUI.EntryRow import EntryRow

class DisplayAction(ActionBase):
    ready = False
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.plugin_base.asset_manager.icons.add_listener(self._icon_changed)
        self.plugin_base.asset_manager.colors.add_listener(self._color_changed)

        self.create_generative_ui()

        self.plugin_base.connect_to_event(
            event_id="com_quintar_streamdeckbutton::AdvancedEvent",
            callback=self.on_label_change
        )

                
    def on_ready(self) -> None:
        log.info("StreamDeck Button Plugin is ready!")
        
        icon_path = os.path.join(self.plugin_base.PATH, "assets", "info.png")
        self.set_media(media_path=icon_path, size=0.75)
        self.display_settings()
        ready = True
        
    def on_key_down(self) -> None:
        pass
    
    def on_key_up(self) -> None:
        self.display_settings()

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

    def create_generative_ui(self) -> None:
        self.ip_row = EntryRow(
            action_core=self,
            var_name="server.ip",
            default_value="localhost",
            title="IP or Hostname",
            auto_add=False,
            complex_var_name=True,
            on_change=self.on_change,
        )
        self.port_row = EntryRow(
            action_core=self,
            var_name="server.port",
            default_value="65432",
            title="Port (Any Number > 1023)",
            auto_add=False,
            complex_var_name=True,
            on_change=self.on_change,
        )

    def on_change(self, widget, new_value, old_value) -> None:
        if(self.ready): self.display_settings()

    def get_config_rows(self) -> List[Any]:
        self.display_settings()
        return [self.ip_row.widget, self.port_row.widget]


    def display_settings(self):
        settings = self.get_settings()
        self.plugin_base.backend.on_advanced_action_triggered(self.ip_row.get_text(), int(self.port_row.get_text()))
        #log.info(f"Current Settings: {settings}")
        self.set_top_label      (self.ip_row.get_text())
        self.set_center_label   (self.port_row.get_text())


    async def on_label_change(self, *args, **kwargs):
        #log.info(f"Label change event received with args: {args} {kwargs}")
        eventName = ""
        labels = []
        if(len(kwargs) >= 2):
            eventName = str(args[0])
            labels = kwargs["data"]

        if(len(labels) >= 1): self.set_top_label   (str(labels[0]))
        if(len(labels) >= 2): self.set_center_label(str(labels[1]))
        if(len(labels) >= 3): self.set_bottom_label(str(labels[2]))