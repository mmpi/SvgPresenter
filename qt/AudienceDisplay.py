from PyQt4 import QtCore
# from PyQt4 import QtGui

from BaseDisplay import BaseDisplay
from SlideArea import SlideArea

class AudienceDisplay(BaseDisplay):
    def __init__(self, presentation):
        BaseDisplay.__init__(self, presentation)
        
        self.slideArea = SlideArea(self, self.presentation)
        self.presentation.slideChange.connect(self.slideArea.showNewSlide)
        self.presentation.startMovie.connect(self.slideArea.startMovie)

        self.setMinimumSize(640, 480)
    
    def resizeEvent(self, event):
        slideSize = self.slideArea.nativeResolution()
        slideSize.scale(self.width(), self.height(), QtCore.Qt.KeepAspectRatio)
        self.slideArea.setGeometry(0.5*(self.width()-slideSize.width()), 0.5*(self.height()-slideSize.height()), slideSize.width(), slideSize.height())

    def mouseDoubleClickEvent (self, event):
        self.setWindowState(self.windowState() ^ QtCore.Qt.WindowFullScreen)