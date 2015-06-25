#!/usr/bin/env python
import sys
from svg.SvgPresentation import SvgPresentation

if len(sys.argv)<2:
    print "Usage: convertToPdf.py <svgfile>"
    print
    sys.exit(1)
else:
    svgPath = sys.argv[1]
    presentation = SvgPresentation(svgPath)
    if presentation.numberOfSlides()<1:
        print "No slides!"
        presentation.cleanUp()
        sys.exit(1)
    
    # create pdf
    presentation.exportAsPdf()    
    presentation.cleanUp()
