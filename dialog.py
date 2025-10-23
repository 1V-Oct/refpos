# align_plugin/dialog.py

import pcbnew
import wx

class AlignDialog(wx.Dialog):
    """
    The main dialog for the Align Tools plugin.
    """
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        # Initialize the dialog
        super().__init__(self.parent_frame, title="Align Tools", style=wx.DEFAULT_DIALOG_STYLE)

        # --- Sizers ---
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        button_sizer = wx.StdDialogButtonSizer()

        # --- Widgets ---
        info_text = wx.StaticText(self, label="Choose label type and alignment options:")

        # Buttons (label names shown in UI)
        self.align_button = wx.Button(self, label="References")
        self.align_values_button = wx.Button(self, label="Values")

        # Alignment mode selector
        self.alignment_modes = ["Left", "Center", "Right"]
        self.alignment_selector = wx.RadioBox(self, label="Horizontal Alignment",
                                              choices=self.alignment_modes,
                                              majorDimension=1, style=wx.RA_SPECIFY_ROWS)

        # Position mode selector (Absolute or Relative)
        self.position_modes = ["Absolute", "Relative"]
        self.position_selector = wx.RadioBox(self, label="Position Mode",
                                             choices=self.position_modes,
                                             majorDimension=1, style=wx.RA_SPECIFY_ROWS)

        # Standard OK and Cancel buttons
        ok_button = wx.Button(self, wx.ID_OK)
        cancel_button = wx.Button(self, wx.ID_CANCEL)

        # --- Layout ---
        main_sizer.Add(info_text, 0, wx.ALL, 10)
        main_sizer.Add(self.align_button, 0, wx.EXPAND | wx.ALL, 10)
        main_sizer.Add(self.align_values_button, 0, wx.EXPAND | wx.ALL, 10)
        main_sizer.Add(self.alignment_selector, 0, wx.EXPAND | wx.ALL, 10)
        main_sizer.Add(self.position_selector, 0, wx.EXPAND | wx.ALL, 10)
        main_sizer.Add(wx.StaticLine(self), 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        button_sizer.AddButton(ok_button)
        button_sizer.AddButton(cancel_button)
        button_sizer.Realize()

        main_sizer.Add(button_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # Finalize
        self.SetSizerAndFit(main_sizer)

        # --- Bind Events ---
        self.align_button.Bind(wx.EVT_BUTTON, self.on_align)
        self.align_values_button.Bind(wx.EVT_BUTTON, self.on_align_values)

    def on_align(self, event):
        """
        This function is called when the 'Align' button is clicked.
        For now, it just shows a message.
        """
        board = pcbnew.GetBoard()

        # Collect selected footprints
        selected_footprints = [fp for fp in board.GetFootprints() if fp.IsSelected()]

        if len(selected_footprints) < 2:
            wx.MessageBox("Please select at least two footprints to align.", "Not enough footprints", wx.OK | wx.ICON_WARNING)
            return

        # Let the user explicitly choose which selected footprint will be the anchor.
        ref_items = [(fp.GetReference() or f"<unnamed {i}>", fp) for i, fp in enumerate(selected_footprints)]
        # Sort by reference name (case-insensitive)
        ref_items.sort(key=lambda t: t[0].upper())
        choices = [name for name, _ in ref_items]
        choice_dlg = wx.SingleChoiceDialog(self,
                                           "Select the anchor footprint (other selected footprints will align to it):",
                                           "Choose Anchor",
                                           choices)
        if choice_dlg.ShowModal() != wx.ID_OK:
            choice_dlg.Destroy()
            return
        anchor_index = choice_dlg.GetSelection()
        choice_dlg.Destroy()

        anchor_fp = ref_items[anchor_index][1]
        footprints_to_align = [fp for name, fp in ref_items if fp is not anchor_fp]

        anchor_ref = anchor_fp.Reference()
        if not anchor_ref:
            wx.MessageBox(f"Anchor footprint {anchor_fp.GetReference()} has no reference text.", "Error", wx.OK | wx.ICON_ERROR)
            return

        # Anchor metrics for horizontal alignment
        anchor_ref_pos = anchor_ref.GetPosition()
        anchor_ref_bbox = anchor_ref.GetBoundingBox()
        anchor_ref_center_x = anchor_ref_pos.x
        anchor_ref_left_x = anchor_ref_center_x - (anchor_ref_bbox.GetWidth() / 2)
        anchor_ref_right_x = anchor_ref_center_x + (anchor_ref_bbox.GetWidth() / 2)

        # Position mode: Absolute or Relative
        pos_mode = self.position_selector.GetString(self.position_selector.GetSelection())
        if pos_mode == "Relative":
            # Compute anchor offset from its footprint center, but take alignment mode into account
            anchor_fp_center_x = anchor_fp.GetPosition().x
            anchor_fp_center_y = anchor_fp.GetPosition().y
            mode = self.alignment_selector.GetString(self.alignment_selector.GetSelection())
            if mode == "Left":
                anchor_ref_left_x = anchor_ref_center_x - (anchor_ref_bbox.GetWidth() / 2)
                anchor_offset_x = anchor_ref_left_x - anchor_fp_center_x
            elif mode == "Center":
                anchor_offset_x = anchor_ref_center_x - anchor_fp_center_x
            else:  # Right
                anchor_ref_right_x = anchor_ref_center_x + (anchor_ref_bbox.GetWidth() / 2)
                anchor_offset_x = anchor_ref_right_x - anchor_fp_center_x

            anchor_offset_y = anchor_ref_pos.y - anchor_fp_center_y

        # Move other references
        moved = 0
        for fp in footprints_to_align:
            ref_to_move = fp.Reference()
            if not ref_to_move:
                continue  # Skip if footprint has no reference

            if pos_mode == "Relative":
                # Place the label according to footprint center + anchor offset, considering alignment
                fp_center_x = fp.GetPosition().x
                fp_center_y = fp.GetPosition().y
                ref_bbox = ref_to_move.GetBoundingBox()
                if mode == "Left":
                    target_left_x = fp_center_x + anchor_offset_x
                    new_x = target_left_x + (ref_bbox.GetWidth() / 2)
                elif mode == "Center":
                    new_x = fp_center_x + anchor_offset_x
                else:  # Right
                    target_right_x = fp_center_x + anchor_offset_x
                    new_x = target_right_x - (ref_bbox.GetWidth() / 2)

                new_y = fp_center_y + anchor_offset_y
            else:
                # Horizontal: compute X based on selected alignment mode
                ref_bbox = ref_to_move.GetBoundingBox()
                mode = self.alignment_selector.GetString(self.alignment_selector.GetSelection())
                if mode == "Left":
                    new_x = anchor_ref_left_x + (ref_bbox.GetWidth() / 2)
                elif mode == "Center":
                    # align centers
                    new_x = anchor_ref_center_x
                else:  # Right
                    new_x = anchor_ref_right_x - (ref_bbox.GetWidth() / 2)

                # Vertical: use the footprint's position Y coordinate as its center
                new_y = fp.GetPosition().y

            ref_to_move.SetPosition(pcbnew.VECTOR2I(int(new_x), int(new_y)))
            moved += 1

        wx.MessageBox(f"Aligned {moved} footprint references to {anchor_fp.GetReference()}.", "Alignment Complete", wx.OK | wx.ICON_INFORMATION)
        self.EndModal(wx.ID_OK)

    def on_align_values(self, event):
        """Align footprint value labels using the same method as references."""
        board = pcbnew.GetBoard()

        # Collect selected footprints
        selected_footprints = [fp for fp in board.GetFootprints() if fp.IsSelected()]

        if len(selected_footprints) < 2:
            wx.MessageBox("Please select at least two footprints to align.", "Not enough footprints", wx.OK | wx.ICON_WARNING)
            return

        # Let the user explicitly choose which selected footprint will be the anchor.
        ref_items = [(fp.GetReference() or f"<unnamed {i}>", fp) for i, fp in enumerate(selected_footprints)]
        ref_items.sort(key=lambda t: t[0].upper())
        choices = [name for name, _ in ref_items]
        choice_dlg = wx.SingleChoiceDialog(self,
                                           "Select the anchor footprint (other selected footprints will align to it):",
                                           "Choose Anchor",
                                           choices)
        if choice_dlg.ShowModal() != wx.ID_OK:
            choice_dlg.Destroy()
            return
        anchor_index = choice_dlg.GetSelection()
        choice_dlg.Destroy()

        anchor_fp = ref_items[anchor_index][1]
        footprints_to_align = [fp for name, fp in ref_items if fp is not anchor_fp]

        anchor_val = anchor_fp.Value()
        if not anchor_val:
            wx.MessageBox(f"Anchor footprint {anchor_fp.GetReference()} has no value text.", "Error", wx.OK | wx.ICON_ERROR)
            return

        # Anchor metrics for horizontal alignment (value)
        anchor_val_pos = anchor_val.GetPosition()
        anchor_val_bbox = anchor_val.GetBoundingBox()
        anchor_val_center_x = anchor_val_pos.x
        anchor_val_left_x = anchor_val_center_x - (anchor_val_bbox.GetWidth() / 2)
        anchor_val_right_x = anchor_val_center_x + (anchor_val_bbox.GetWidth() / 2)

        # Position mode
        pos_mode_val = self.position_selector.GetString(self.position_selector.GetSelection())
        if pos_mode_val == "Relative":
            anchor_fp_center_x = anchor_fp.GetPosition().x
            anchor_fp_center_y = anchor_fp.GetPosition().y
            mode_val = self.alignment_selector.GetString(self.alignment_selector.GetSelection())
            if mode_val == "Left":
                anchor_val_left_x = anchor_val_center_x - (anchor_val_bbox.GetWidth() / 2)
                anchor_offset_x = anchor_val_left_x - anchor_fp_center_x
            elif mode_val == "Center":
                anchor_offset_x = anchor_val_center_x - anchor_fp_center_x
            else:
                anchor_val_right_x = anchor_val_center_x + (anchor_val_bbox.GetWidth() / 2)
                anchor_offset_x = anchor_val_right_x - anchor_fp_center_x

            anchor_offset_y = anchor_val_pos.y - anchor_fp_center_y

        # Move other values
        moved = 0
        for fp in footprints_to_align:
            val_to_move = fp.Value()
            if not val_to_move:
                continue  # Skip if footprint has no value

            if pos_mode_val == "Relative":
                fp_center_x = fp.GetPosition().x
                fp_center_y = fp.GetPosition().y
                val_bbox = val_to_move.GetBoundingBox()
                if mode_val == "Left":
                    target_left_x = fp_center_x + anchor_offset_x
                    new_x = target_left_x + (val_bbox.GetWidth() / 2)
                elif mode_val == "Center":
                    new_x = fp_center_x + anchor_offset_x
                else:
                    target_right_x = fp_center_x + anchor_offset_x
                    new_x = target_right_x - (val_bbox.GetWidth() / 2)

                new_y = fp_center_y + anchor_offset_y
            else:
                # Horizontal: compute X based on selected alignment mode
                val_bbox = val_to_move.GetBoundingBox()
                mode = self.alignment_selector.GetString(self.alignment_selector.GetSelection())
                if mode == "Left":
                    new_x = anchor_val_left_x + (val_bbox.GetWidth() / 2)
                elif mode == "Center":
                    new_x = anchor_val_center_x
                else:  # Right
                    new_x = anchor_val_right_x - (val_bbox.GetWidth() / 2)

                # Vertical: use the footprint's position Y coordinate as its center
                new_y = fp.GetPosition().y

            val_to_move.SetPosition(pcbnew.VECTOR2I(int(new_x), int(new_y)))
            moved += 1

        wx.MessageBox(f"Aligned {moved} footprint values to {anchor_fp.GetReference()}.", "Alignment Complete", wx.OK | wx.ICON_INFORMATION)
        self.EndModal(wx.ID_OK)
