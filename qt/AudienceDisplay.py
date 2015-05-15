from PyQt4 import QtCore
# from PyQt4 import QtGui

from BaseDisplay import BaseDisplay
from SlideArea import SlideArea

class AudienceDisplay(BaseDisplay):
    def __init__(self, presentationController):
        BaseDisplay.__init__(self, presentationController)
        
        self.slideArea = SlideArea(self, self.presentationController)
        self.presentationController.slideChange.connect(self.slideArea.showNewSlide)
        self.presentationController.startMovie.connect(self.slideArea.startMovie)

        self.setMinimumSize(640, 480)
        self.resize(self.slideArea.preferredSize())
       
    
    def resizeEvent(self, event):
        slideSize = self.slideArea.preferredSize(self.size())
        self.slideArea.setGeometry(0.5*(self.width()-slideSize.width()), 0.5*(self.height()-slideSize.height()), slideSize.width(), slideSize.height())

    def mouseDoubleClickEvent (self, event):
        self.setWindowState(self.windowState() ^ QtCore.Qt.WindowFullScreen)