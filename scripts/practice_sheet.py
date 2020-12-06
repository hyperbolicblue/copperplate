# -*- coding: utf-8 -*-
# author: hyperbolicblue <hyperbolicblue@protonmail.com>
#
# This file is licensed under: BSD 3-Clause License.
# Copyright (c) 2020, hyperbolicblue <hyperbolicblue@protonmail.com>
# All rights reserved.
# See <https://github.com/hyperbolicblue/copperplate>

"""Create a practice sheet filled with guidelines for Copperplate calligraphy
and write it to file."""
__version__ = '1.0'

import os
import sys
import logging
import argparse
from argparse import RawTextHelpFormatter
import numpy as np
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)

plt.rcParams['savefig.format'] = 'pdf'

MMPERINCH = 25.4 # in / mm; 1 in = 25.4 mm


def parse_args(sysargs):
    """Parse command line arguments and return .

    Args:
        sysargs (list): list of command line arguments

    Returns:
        argparse.Namespace: parsed arguments

    """
    parser = argparse.ArgumentParser(
                 description='Create a practice sheet with guidelines for '
                             'Copperplate calligraphy and write it to file.',
                 epilog='defaults:\n'
                        '  UNIT                 mm\n'
                        '  WIDTH HEIGHT         210 197\n'
                        '  ORIENTATION          portrait\n'
                        '  X-HEIGHT             1.0\n'
                        '  DESC X ASC           3 2 3\n'
                        '  LINEWIDTH            1.0\n'
                        '  LINECOLOR            k\n'
                        '  LINESTYLE            --\n'
                        '  TOPMARGIN            10.0\n'
                        '  VERTICALMARGIN       5.0\n'
                        '  GAP                  4.0\n'
                        '  SLANTANGLE           55.0\n'
                        '  SLANTSPACE           13.0\n'
                        '\n\n'
                        'examples:\n'
                        '  - use defaults:\n'
                        '    python {pname} my_practice_sheet.pdf\n'
                        '  - use ANSI Letter for paper size:\n'
                        '    python {pname} -u in -p 8.5 11 my_practice_sheet.pdf\n'
                        '  - use different ratios between line heights and red lines:\n'
                        '    python {pname} -r 2 1.5 2 -c r my_practice_sheet.pdf\n'
                        '\n\n'
                        'Version {}.'
                        '\n\n'
                        'Copyright (c) 2020, '
                        'hyperbolicblue <hyperbolicblue@protonmail.com>.\n'
                        'All rights reserved. Licensed under '
                        'BSD 3-Clause License.\n'
                        '\n\n'
                        'Please report bugs to '
                        '<https://github.com/hyperbolicblue/copperplate/issues>'
                        .format(__version__, pname=os.path.basename(__file__)),
                 formatter_class=RawTextHelpFormatter)
    parser.add_argument('output', type=str,
                        help='name of output file (use -f to force overwrite)')
    parser.add_argument('-a', '--annotate', action='store_true',
                        help='add sheet information at the bottom of the page')
    parser.add_argument('-f', '--force', action='store_true',
                        help="overwrite output if file already exists")
    parser.add_argument('-n', '--noslantlines', action='store_true',
                        help="omit slant lines")
    parser.add_argument('-u', choices=['mm', 'in'], default='mm', dest='unit',
                        metavar='UNIT', help="unit of length, from {mm, in}'")
    parser.add_argument('-p', nargs=2, type=float, metavar=('WIDTH', 'HEIGHT'),
                        dest='papersize', help="papersize in unit UNIT")
    parser.add_argument('-o', choices=['landscape', 'portrait'],
                        default='portrait', metavar='ORIENTATION',
                        dest='orientation',
                        help="paper orientation, from {'portrait', 'landscape'}")
    parser.add_argument('-x', type=float, metavar='X-HEIGHT', dest='xheight',
                        help="height of the letter 'x'")
    parser.add_argument('-r', type=float, nargs=3, default=[3, 2, 3],
                        metavar=('DESC', 'X', 'ASC'), dest='ratio',
                        help='ratios descender : x-height : ascender')
    parser.add_argument('-w', type=float, metavar='LINEWIDTH',
                        dest='linewidth', help='line width')
    parser.add_argument('-c', type=str, default='k', metavar='LINECOLOR',
                        dest='linecolor', help="line color")
    parser.add_argument('-l', type=str, default='--', metavar='LINESTYLE',
                        dest='linestyle',
                        help='style of ascender and descender lines')
    parser.add_argument('-t', type=float, metavar='TOPMARGIN',
                        dest='topmargin',
                        help='margin on the top of the page')
    parser.add_argument('-v', type=float, metavar='VERTICALMARGIN',
                        dest='verticalmargin',
                        help='left and right margin')
    parser.add_argument('-g', type=float, metavar='GAP', dest='gap',
                        help='vertical gap between each set of lines')
    parser.add_argument('-s', type=float, default=55.0, metavar='SLANTANGLE',
                        dest='slantangle',
                        help='slant angle (deg, positive from horizontal)')
    parser.add_argument('-k', type=float, metavar='SLANTLINESPACING',
                        dest='slantlinespacing',
                        help='horizontal space between slant lines')
    parsedargs = parser.parse_args(sysargs)

    if os.path.isfile(parsedargs.output) and not parsedargs.force:
        raise OSError('{} already exists. Use --force to overwrite.' \
                      .format(parsedargs.output))
    wrappedangle = parsedargs.slantangle % 360
    if wrappedangle and (wrappedangle < 5 or wrappedangle > 350 - 5):
        raise ValueError('The slant angle ({} deg) is too small. '
                         'Please enter a value between 5 and 355 (modulo 360).'
                         .format(parsedargs.slantangle))
    parsedargs.ratio = np.array(parsedargs.ratio[::-1]) # descender, x-height, ascender

    # set defaults (dependent on choice for 'unit'):
    if parsedargs.papersize is None:
        parsedargs.papersize = np.array([210, 297]) / (1 if parsedargs.unit == 'mm' else MMPERINCH)
    if parsedargs.topmargin is None:
        parsedargs.topmargin = 10.0 / (1 if parsedargs.unit == 'mm' else MMPERINCH)
    if parsedargs.verticalmargin is None:
        parsedargs.verticalmargin = 5.0  / (1 if parsedargs.unit == 'mm' else MMPERINCH)
    if parsedargs.xheight is None:
        parsedargs.xheight = 6.0  / (1 if parsedargs.unit == 'mm' else MMPERINCH)
    if parsedargs.slantlinespacing is None:
        parsedargs.slantlinespacing = 13.0  / (1 if parsedargs.unit == 'mm' else MMPERINCH)
    if parsedargs.gap is None:
        parsedargs.gap = 4.0  / (1 if parsedargs.unit == 'mm' else MMPERINCH)
    if parsedargs.linewidth is None:
        parsedargs.linewidth = 1.0

    parsedargs.linewidth *= 10 / (1 if parsedargs.unit == 'mm' else MMPERINCH)
    parsedargs.papersize = np.array(parsedargs.papersize)
    if parsedargs.orientation == 'landscape':
        parsedargs.papersize = parsedargs.papersize[::-1]
    return parsedargs


def plot_set(axes, ascenderxleft, ascenderyleft):
    """Plot a set of lines.

    A set of lines contains descender line, baseline, median, ascender
    line, all slanted lines, and veritcal delimiters at the beginning and at
    the end of the horizontal lines.

    Args:
        axes (matplotlib.axes._axes.Axes): Axes
        ascenderxleft (float): x coordinate of left end of ascender line
        ascenderyleft (float): y coordinate of left end of ascender line

    Returns:
        --

    """
    ascenderxright = args.papersize[0] - ascenderxleft
    heights = args.ratio / args.ratio[1] * args.xheight
    setheight = np.sum(heights)

    def plot_horizontals():
        """Plot all horizontal lines.

        Horizontal lines are descender, baseline, median, ascender, and
        slanted lines.

        """
        xcoords = np.array([ascenderxleft, ascenderxright])
        ycoords = np.array(2 * [args.papersize[1] - ascenderyleft])
        for counter, yshift in enumerate([0] + list(np.cumsum(heights))):
            axes.plot(xcoords, ycoords - yshift, '-', color=args.linecolor,
                    linewidth=args.linewidth,
                    linestyle='-' if counter in {1, 2} else args.linestyle)

    def plot_verticals():
        """Plot vertical lines at the beginning and at the end of each set of
        horizontal lines."""
        xcoords = [ascenderxleft, ascenderxright]
        ycoords = [args.papersize[1] - ascenderyleft, args.papersize[1] - ascenderyleft - setheight]
        for index in [0, 1]:
            axes.plot([xcoords[index], xcoords[index]], ycoords,
                    '-', color=args.linecolor, linewidth=args.linewidth)

    def plot_slanted_lines():
        """Plot all slanted lines.

        Tilted lines on different sets are part of the same linear function.

        """
        slope = np.tan(args.slantangle / 180 * np.pi)
        slopesign = np.sign(slope)
        run = setheight / slope # 'rise over run' = 'setheight over run'
        descender_ypos = args.papersize[1] - ascenderyleft - setheight # y position of descender
        def trim_line(xcoords, ycoords):
            """Adjust coordinates of they are partly out of plot range."""
            if not (xcoords[0] >= ascenderxleft and
                    xcoords[1] <= ascenderxright): # trim for slope > 0
                if xcoords[0] < ascenderxleft: # trim to the left
                    ycoords[0] = slope * (ascenderxleft - xcoords[0]) + ycoords[0]
                    xcoords[0] = ascenderxleft
                if xcoords[1] > ascenderxright: # trim to the right
                    ycoords[1] = slope * (ascenderxright - xcoords[0]) + ycoords[0]
                    xcoords[1] = ascenderxright
            if not (xcoords[0] <= ascenderxright and
                    xcoords[1] >= ascenderxleft): # trim for slope < 0
                if xcoords[0] > ascenderxright: # trim to the right
                    ycoords[0] = slope * (ascenderxright - xcoords[0]) + ycoords[0]
                    xcoords[0] = ascenderxright
                if xcoords[1] < ascenderxleft: # trim to the left
                    ycoords[1] = slope * (ascenderxleft - xcoords[0]) + ycoords[0]
                    xcoords[1] = ascenderxleft
            return xcoords, ycoords

        def shift_slantline_into_plotrange():
            """Bring intersection of slantline and descender in plot range.

            The slantline is (in paper coordinates) parameterized as

                y = slope * x + b,

            where slantangle defines the slope and the intersection with the
            descender line can be adjusted by changing b. Since slope lines are
            equidistant in x, b changes in multiples of slantlinespacing.

            Returns:
                float: x coordinate of intersection with descender that is
                    within the given plot range.

            """
            # xcwsid: X Coordinate Where Slantline Intersects Descender
            xcwsid = ycwsid / slope + \
                     10 * slopesign * args.slantlinespacing # to avoid edge cases
            while not any(ascenderxleft < xpos < ascenderxright
                          for xpos in [xcwsid, xcwsid + run]
                          ): # slantline completely out of plot range
                xcwsid -= slopesign * args.slantlinespacing
            return xcwsid

        ycwsid = descender_ypos
        xcwsid = shift_slantline_into_plotrange()
        # plot and shift in both directions until slantline leaves plot range
        initialxcswid = xcwsid
        for direction in [1, -1]:
            xcwsid = initialxcswid
            if direction == 1: # avoid plotting the initial line twice
                xcwsid += direction * args.slantlinespacing
            while any(ascenderxleft < xpos < ascenderxright
                      for xpos in [xcwsid, xcwsid + run]
                      ): # slantline (at least partly) in plot range
                xcoords = xcwsid + np.array([0, run])
                ycoords = [descender_ypos, descender_ypos + setheight]

                xcoords, ycoords = trim_line(xcoords, ycoords)
                axes.plot(xcoords, ycoords, '-', color=args.linecolor,
                        linewidth=args.linewidth)
                xcwsid += direction * args.slantlinespacing

    plot_horizontals()
    plot_verticals()
    if not (args.noslantlines or args.slantangle in [0, 180]):
        plot_slanted_lines()


def annotate_plot(axes, textposx, textposy):
    """Annotate plot with a line of informational text.

    Args:
        axes (matplotlib.axes._axes.Axes): Axes
        textposx (float): x coordinate of right-aligned text
        textposy (float): y coordinate of right-aligned text

    Returns:
        --

    """
    if args.orientation == 'portrait':
        textposx *= 1.02
    paperx, papery = args.papersize
    xheight = args.xheight
    line = 'papersize = {} x {} {unit}, ' \
           'x-height = {} {unit}, ' \
           'slant line spacing = {} {unit}, {}' \
           'height ratios (descender : x : ascender) = {}:{}:{}, ' \
           'slant angle (from horizontal) = {} deg [v{version}]' \
           .format(np.round(paperx, 2), np.round(papery, 2),
                   np.round(xheight, 2),
                   np.round(args.slantlinespacing, 2),
                   '\n' if args.orientation == 'portrait' else '',
                   *np.round(args.ratio, 2),
                   np.round(args.slantangle, 2),
                   unit=args.unit,
                   version=__version__)
    windowy1, windowy2 = plt.gca().get_window_extent().get_points()[:, 1]
    windowyscale = (windowy2 - windowy1) # assumes axes size of 1
    fontsize = 0.01 * windowyscale
    axes.text(textposx, textposy, line, color='gray', fontsize=fontsize,
           horizontalalignment='right')


def main():
    """Create a practice sheet filled with guidelines for Copperplate
    calligraphy and write it to file."""
    lineset_height = args.gap + np.sum(args.ratio / args.ratio[1] *
                                       args.xheight)
    number_of_linesets = int(np.floor((args.papersize[1] -
                                       args.topmargin) / lineset_height))

    fig = plt.figure(figsize=args.papersize)
    axes = fig.add_axes([0.0, 0.0, 1.0, 1.0], frameon=False) # normalized lengths
    for linesetindex in range(number_of_linesets):
        lineset_topmargin = args.topmargin + linesetindex * lineset_height
        plot_set(axes, args.verticalmargin, lineset_topmargin)
    if args.annotate:
        textposx = args.papersize[0] - 2 * args.verticalmargin
        textposy = 0.01 * args.papersize[1]
        annotate_plot(axes, textposx, textposy)
    axes.set_xlim([0, args.papersize[0]])
    axes.set_ylim([0, args.papersize[1]])
    axes.set_aspect('equal')
    axes.set_xticks([])
    axes.set_yticks([])
    axes.set_xticklabels([])
    axes.set_yticklabels([])
    plt.savefig(args.output)


if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    main()
