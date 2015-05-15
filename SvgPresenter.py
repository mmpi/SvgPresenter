#!/usr/bin/env python
import sys
from PyQt4 import QtGui

from svg.SvgPresentation import SvgPresentation
from qt.PresentationController import PresentationController
from qt.AudienceDisplay import AudienceDisplay

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
    presentation.exportAsPdf()    
        
    app = QtGui.QApplication(sys.argv)
    pc = PresentationController(presentation)
    ad1 = AudienceDisplay(pc)
    ad1.show()
    # ad2 = AudienceDisplay(presentation)
    # ad2.show()
    # ad.showFullScreen()
     
    ret = app.exec_()
    presentation.cleanUp()
    sys.exit(ret)
