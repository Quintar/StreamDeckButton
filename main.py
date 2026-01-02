# Import StreamController modules
import os
from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.PluginManager.ActionHolder import ActionHolder

# Import actions
from .actions.DisplayAction.DisplayAction import DisplayAction

class StreamDeckButton(PluginBase):
    def __init__(self):
        super().__init__()
        backend_path = os.path.join(self.PATH, "backend", "backend.py") 
        self.launch_backend(backend_path=backend_path, open_in_terminal=False) #set to False in production
        
        ## Register actions
        self.display_action_holder = ActionHolder(
            plugin_base = self,
            action_base = DisplayAction,
            action_id = "com_quintar_streamdeckbutton::DisplayAction",
            action_name = "Display Action",
        )
        self.add_action_holder(self.display_action_holder)

        # Register plugin
        self.register(
            plugin_name = "Template",
            github_repo = "https://github.com/Quintar/StreamDeckPlugin",
            plugin_version = "1.0.0",
            app_version = "1.15.0-alpha"
        )