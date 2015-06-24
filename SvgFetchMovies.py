#!/usr/bin/env python
import sys

from svg.SvgManipulations import fetchAllMovies

# Mode = "svg"
Mode = "svgRaster"

if len(sys.argv)<2:
    print "Usage: SvgFetchMovies.py <svgfile>"
    print
    sys.exit(1)
else:
    fetchAllMovies(sys.argv[1], sys.argv[2:])
