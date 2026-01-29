from gi.repository import Gtk, Adw
import gi
from typing import Any

from loguru import logger as log

from src.backend.PluginManager import PluginBase

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

KEY_FILE_PATH = "file_path"             #settings key
KEY_CHECK_INTERVAL = "check_interval"   #settings key

class PluginSettings:
    _file_path: Adw.EntryRow
    _check_interval: Adw.EntryRow

    def __init__(self, plugin_base: PluginBase) -> None:
        self._plugin_base: PluginBase = plugin_base


    def get_settings_area(self) -> Adw.PreferencesGroup:
        self._file_path = Adw.EntryRow(
            title=self._plugin_base.lm.get("preferences.file_path")
        )

        adjustment = Gtk.Adjustment.new(1.0, 0.0, 10000.0, 1.0, 10.0, 0.0)
        
        self._check_interval = Adw.SpinRow(
            title=self._plugin_base.lm.get("preferences.interval_title"),
            adjustment=adjustment
        )

        self._file_path.connect("notify::text", self._on_change_file_path)
        self._check_interval.connect("notify::text", self._on_change_check_interval)

        self._load_settings()

        pref_group = Adw.PreferencesGroup()
        pref_group.set_title(self._plugin_base.lm.get("preferences.title"))
        pref_group.add(self._file_path)
        pref_group.add(self._check_interval)
        return pref_group
    
    def _load_settings(self) -> None:
        settings = self._plugin_base.get_settings()
        file_path = settings.get(KEY_FILE_PATH, "")
        interval = settings.get(KEY_CHECK_INTERVAL, "1.0")
        self._file_path.set_text(file_path)
        self._check_interval.set_value(float(interval))
        self._set_settings_on_backend(settings)


    def _update_settings(self, key: str, value: str) -> None:
        settings = self._plugin_base.get_settings()
        settings[key] = value
        self._plugin_base.set_settings(settings)

    def _on_change_file_path(self, entry: Any, _: Any) -> None:
        val = entry.get_text().strip()
        self._update_settings(KEY_FILE_PATH, val)

    def _on_change_check_interval(self, entry: Any, _: Any) -> None:
        val = entry.get_text().strip()
        self._update_settings(KEY_CHECK_INTERVAL, float(val))

    def _set_settings_on_backend(self, settings):
        self._plugin_base.trigger_event_settings_changed(
            event_id="com_quintar_streamdeckbutton::SettingsChangedEvent",
            data=(settings.get(KEY_FILE_PATH, ""), settings.get(KEY_CHECK_INTERVAL, "1.0"))
        )
