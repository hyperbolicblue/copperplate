# copperplate

This package provides a simple and flexible tool for creating practice sheets
for Copperplate calligraphy.

# License

This package is licensed under BSD 3-Clause License and may be used under that
license; see LICENSE.sig for details.

# scripts/practice_sheet.py
This module creates a pdf file with a practice sheet for Copperplate
calligraphy.

The default output format is pdf. The following options can be customized
using the command-line interface:
  * papersize
  * orientation (portrait or landscape)
  * x-height
  * ratios between descender, x-height, and ascender
  * line width, color, and style
  * page marigins
  * gap between sets of lines
  * slant line angle and spacing
  * slant lines can be switched off
  * sheet information at the bottom of the sheet can be switched on

See practice_sheet.py -h for details.

# Dependencies
The module scripts/practice_sheet.py imports numpy and matplotlib.pyplot, and
is tested with Python 3.9.0.
