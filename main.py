# Import StreamController modules
from typing import Any
from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.PluginManager.ActionHolder import ActionHolder
from src.backend.PluginManager.EventHolder import EventHolder
from loguru import logger as log

from .settings_file import KEY_FILE_PATH, PluginSettings

import os

# Import actions
from .actions.DisplayAction.DisplayAction import DisplayAction

class StreamDeckButton(PluginBase):
    def __init__(self):
        super().__init__()

        self.has_plugin_settings = True
        self.lm = self.locale_manager
        self.lm.set_to_os_default()

        self.prepare_backend()

        self._settings_manager: PluginSettings = PluginSettings(self)

        ## Register actions
        self.display_action_holder = ActionHolder(
            plugin_base = self,
            action_base = DisplayAction,
            action_id = "com_quintar_streamdeckbutton::DisplayAction",
            action_name = "Display Action",
        )
        self.add_action_holder(self.display_action_holder)

        self._event_holder = EventHolder(
            plugin_base=self,
            event_id="com_quintar_streamdeckbutton::AdvancedEvent",
        )
        self.add_event_holder(self._event_holder)

        # Register plugin
        self.register(
            plugin_name = "StreamDeck Button",
            github_repo = "https://github.com/Quintar/StreamDeckButton",
            plugin_version = "1.0.0",
            app_version = "1.15.0-alpha"
        )

    def trigger_event(self, event_id: str, data: Any):
        self._event_holder.trigger_event(event_id=event_id, data=data)

    def get_settings_area(self) -> Any:
        return self._settings_manager.get_settings_area()
    
    def prepare_backend(self) -> bool:
        # Backend
        backend_path = os.path.join(self.PATH, "backend", "backend_file.py") 
        self.launch_backend(
            backend_path=backend_path, 
            #venv_path=os.path.join(self.PATH, ".venv"),
            open_in_terminal=False)
        self.wait_for_backend(tries=5)

        if (self.backend_connection is None):
            log.error("Backend setup timeout")
            return False
        log.info("Backend setup...")
        settings = self.get_settings()
        file_path = settings.get(KEY_FILE_PATH, "~/lines.txt")
        self.backend.set_path(file_path)

        return True
        
