# Import StreamController modules
import os
from .internal.LabelChangeEventListener import LabelChangeEvent
from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.PluginManager.ActionHolder import ActionHolder

# Import actions
from .actions.DisplayAction.DisplayAction import DisplayAction

class StreamDeckButton(PluginBase):
    def __init__(self):
        super().__init__()
        
        ## Register actions
        self.display_action_holder = ActionHolder(
            plugin_base = self,
            action_base = DisplayAction,
            action_id = "com_quintar_streamdeckbutton::DisplayAction",
            action_name = "Display Action",
        )
        self.add_action_holder(self.display_action_holder)

        # Events
        self.text_change_event_holder = LabelChangeEvent(
            self,
            "com_quintar_streamdeckbutton::LabelChangeEvent"
        )
        self.add_event_holder(self.text_change_event_holder)

        # Register plugin
        self.register(
            plugin_name = "StreamDeck Button",
            github_repo = "https://github.com/Quintar/StreamDeckButton",
            plugin_version = "1.0.0",
            app_version = "1.15.0-alpha"
        )