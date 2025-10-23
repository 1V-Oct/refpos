RefPos — Reference & Value Alignment plugin for KiCad
=====================================================

A small KiCad plugin (Python) to quickly align footprint reference designators (RefDes) and value labels on the PCB editor.

Overview
--------
- Align reference designators (Reference) of multiple selected footprints to a chosen anchor footprint.
- Align value labels (Value) the same way — a separate button.
- Horizontal alignment modes: Left, Center, Right.
- Vertical alignment: centers the label vertically on its footprint position.

This plugin was developed for KiCad 9.0 but uses simple pcbnew API calls and should be compatible with recent KiCad 6/7/8/9 branches (see notes).

Features
--------
- Pick an anchor from the current selection (avoids depending on selection iteration order).
- Align References or Values only (footprints themselves remain unchanged).
- Choose horizontal alignment mode (Left / Center / Right) from the dialog.
 - Choose horizontal alignment mode (Left / Center / Right) from the dialog.
 - Choose position mode: Absolute (align to anchor's absolute label position) or Relative (apply anchor's offset from its footprint center to other footprints).
- Simple, fast, undoable changes inside KiCad.

Vertical (rotated) labels
-------------------------
- The plugin now supports anchors that are rotated 90° (vertical labels). When an anchor label is detected as vertical the alignment logic is applied as if everything were rotated 90°:
   - The label's long axis becomes the alignment axis. Left/Center/Right map to Top/Center/Bottom for the rotated case.
   - In Absolute mode the plugin aligns other labels' Y positions to the anchor's top/center/bottom (and uses each footprint's X center for the cross axis).
   - In Relative mode the anchor's offsets are computed relative to its footprint center and applied to other footprints with edge-aware adjustments (using text height for vertical alignment).

Detection heuristic
-------------------
- The plugin detects a vertical label by comparing the label's bounding-box height and width. If height > width the label is treated as vertical. This avoids relying on KiCad API angle properties and works reliably for typical footprint labels.

Testing and tips for vertical anchors
-----------------------------------
1. Make an anchor label vertical (rotate its Reference or Value 90°) in the footprint properties.
2. Select multiple footprints and run the plugin (References or Values). Choose Absolute or Relative and pick the vertical anchor.
3. Left → maps to Top, Right → maps to Bottom when the anchor is vertical. Center remains center.

If you see small systematic offsets, the plugin can be switched to angle-based detection (uses label angle) or adjusted to consider text origin/pivot — tell me which you prefer and I can add it.

Installation
------------
1. Copy the plugin folder `com_github_duddie_RefPos` into your KiCad plugins directory. Typical locations:
   - Linux/macOS: ~/.local/share/kicad/ or ~/.kicad/...
   - Windows: %APPDATA%\kicad\...

2. In KiCad's PCB editor (Pcbnew) open the "Scripting Console" → "Plugin and Content Manager" and make sure the plugin appears in the list. You can also restart KiCad.

3. Run the plugin from the Tools → External Plugins menu (or toolbar if available).

Usage
-----
1. In Pcbnew, select two or more footprints whose labels you want to align.
2. Open the plugin (Tools → External Plugins → Align Tools).
3. Choose horizontal alignment mode (Left/Center/Right) in the dialog.
4. Click one of the label buttons:
   - References — to align reference designators (Reference texts)
   - Values — to align value labels (Value texts)
5. When the anchor-selection dialog appears, pick which of the selected footprints should be used as the anchor. The plugin will align other selected labels to that anchor.

Notes and tips
--------------
- The plugin only moves text items (Reference/Value). It does not rotate footprints or modify silkscreen.
- Make sure the footprint you intend to use as the anchor actually contains a Reference (or Value) text, otherwise pick another anchor.
- The vertical alignment uses the footprint position Y as the vertical center. If a footprint's text is pinned/locked by its footprint definition, the plugin won't be able to move it.
 - The vertical alignment uses the footprint position Y as the vertical center in Absolute mode. In Relative mode the vertical offset of the anchor label from its footprint center is applied to other footprints as well.

Development / Contributing
--------------------------
- The plugin is implemented in Python and intended to be run inside KiCad's Python environment (pcbnew).
- Bug reports, pull requests and suggestions are welcome. 

License
-------
MIT
