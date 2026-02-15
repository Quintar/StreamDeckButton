# Import StreamController modules
import random

from GtkHelper.GenerativeUI.EntryRow import EntryRow
from GtkHelper.GenerativeUI.SpinRow import SpinRow

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_reader = ReadFileContinously()

        # This is just to provide base functionality
        self.plugin_base.asset_manager.icons.add_listener(self._icon_changed)
        self.plugin_base.asset_manager.colors.add_listener(self._color_changed)

        self.file_path_entry = EntryRow(self, "file_path", "", title="File Path", on_change=self.on_settings_changed)
        self.refresh_spinner = SpinRow(self, "refresh_interval", 1.0, 0.1, 10.0, title="Refresh Interval", on_change=self.on_settings_changed)
                
    def on_ready(self) -> None:
        self._set_file_reader_settings(self.file_path_entry.get_text(), self.refresh_spinner.get_number())
        self.file_reader.start()
        
    def on_key_up(self) -> None:
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

    def on_tick(self):
        self.set_top_label(str(self.file_reader.top_label))
        self.set_center_label(str(self.file_reader.center_label))
        self.set_bottom_label(str(self.file_reader.bottom_label))


    def on_settings_changed(self, *args, **kwargs):
        log.info(f"Args: {kwargs}")
        self._set_file_reader_settings(self.file_path_entry.get_text(), self.refresh_spinner.get_number())
        
    def _set_file_reader_settings(self, file_path, interval):
        self.file_reader.set_path(file_path)
        self.file_reader.set_interval(interval)
