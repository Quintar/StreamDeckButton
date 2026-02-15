# Import StreamController modules

from typing import Any
from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.PluginManager.ActionHolder import ActionHolder
from src.backend.PluginManager.EventHolder import EventHolder

# Import settings
# Import actions
from .actions.DisplayAction.DisplayAction import DisplayAction

class StreamDeckButton(PluginBase):
    def __init__(self):
        super().__init__()

        self.lm = self.locale_manager
        self.lm.set_to_os_default()

        # Register actions
        self.display_action_holder = ActionHolder(
            plugin_base = self,
            action_base = DisplayAction,
            action_id = "com_quintar_streamdeckbutton::DisplayAction",
            action_name = "Display Action",
        )
        self.add_action_holder(self.display_action_holder)

        self._event_holder_settings_changed = EventHolder(
            plugin_base=self,
            event_id="com_quintar_streamdeckbutton::SettingsChangedEvent",
        )
        self.add_event_holder(self._event_holder_settings_changed)


        # Register plugin
        self.register(
            plugin_name = "StreamDeck Button",
            github_repo = "https://github.com/Quintar/StreamDeckButton",
            plugin_version = "1.0.0",
            app_version = "1.15.0-alpha"
        )

    # WARNING EVENTS ARE BROCKEN! They create internal file handles that aren't being destroyed unless you change the screen
    # DON'T USE UNTIL FURTHER NOTICE

    def trigger_event_settings_changed(self, event_id: str, data: Any):
        self._event_holder_settings_changed.trigger_event(event_id=event_id, data=data)    