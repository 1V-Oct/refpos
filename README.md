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
- Bug reports, pull requests and suggestions are welcome. If you publish this repository, add issues or PRs on GitHub.

License
-------
MIT — see LICENSE (if you add one) or consider this a permissive MIT-style plugin.

Contact
-------
If you want changes or additional alignment modes (e.g. align relative to footprint bounding boxes, offset values, or align rotation), open an issue or contact the author.


Enjoy — and let me know if you want automatic offsets or presets per footprint type.