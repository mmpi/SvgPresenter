#!/usr/bin/env python
import sys
from PyQt4 import QtGui

from svg.SvgPresentation import SvgPresentation
from qt.PresentationController import PresentationController
from qt.AudienceDisplay import AudienceDisplay
from qt.PresenterDisplay import PresenterDisplay

# Mode = "svg"
Mode = "svgRaster"

if len(sys.argv)<2:
    print "Usage: SvgPresenter.py <svgfile>"
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
#     presentation.exportAsPdf()    
        
    print "Using mode \"%s\"."%Mode
    print
    
    app = QtGui.QApplication(sys.argv)
    desktop = app.desktop()
    pc = PresentationController(presentation, Mode)
    pd = PresenterDisplay(desktop, pc)
    pd.show()
    ad = AudienceDisplay(desktop, pc)
    ad.show()
#     ad.showFullScreen()
     
    ret = app.exec_()
    presentation.cleanUp()
    sys.exit(ret)
