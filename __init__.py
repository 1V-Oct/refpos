# align_plugin/__init__.py

import os
import pcbnew
import wx
from .dialog import AlignDialog

class AlignPlugin(pcbnew.ActionPlugin):
    """
    A KiCad Action Plugin to align footprints and other items.
    """

    def defaults(self):
        """
        Define the plugin's metadata.
        """
        self.name = "Align Tools"
        self.category = "Alignment"
        self.description = "A plugin to align footprints, text, and other board items."
        self.show_toolbar_button = True # Set to True if you want a toolbar icon
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'icon.png')

    def Run(self):
        """
        This method is called when the user runs the plugin.
        """
        # Create and show the dialog without needing the frame
        dialog = AlignDialog(None)
        # ShowModal blocks until the dialog is closed
        result = dialog.ShowModal()
        dialog.Destroy() # Make sure to destroy the dialog to free memory

        if result == wx.ID_OK:
            pcbnew.Refresh()

# This is the standard way to register the plugin in KiCad
AlignPlugin().register()
