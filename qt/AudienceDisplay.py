from PyQt4 import QtCore, QtGui

from BaseDisplay import BaseDisplay
from SlideArea import SlideArea
from BufferedSlideArea import BufferedSlideArea

class AudienceDisplay(BaseDisplay):
    def __init__(self, desktop, presentationController):
        BaseDisplay.__init__(self, desktop, presentationController)
        self.setWindowTitle("Audience display")
        
#         self.slideArea = SlideArea(self, self.presentationController)
        self.slideArea = BufferedSlideArea(self, self.presentationController)
        self.presentationController.slideChange.connect(self.slideArea.showNewSlide)
        self.presentationController.startMovie.connect(self.slideArea.startMovie)
        self.presentationController.toggleAudienceDisplay.connect(self.slideArea.toggleVisible)

        self.setMinimumSize(640, 480)
        self.resize(self.slideArea.preferredSize())
        self.putOnRightScreen()
    
    def resizeEvent(self, event):
        slideSize = self.slideArea.preferredSize(self.size())
        self.slideArea.setGeometry(0.5*(self.width()-slideSize.width()), 0.5*(self.height()-slideSize.height()), slideSize.width(), slideSize.height())

    def mouseDoubleClickEvent (self, event):
        self.setWindowState(self.windowState() ^ QtCore.Qt.WindowFullScreen)
        
    def putOnRightScreen(self, size=None):
        self.putOnScreen(self.otherScreenIndex(self.primaryScreenIndex()))

    def changeEvent(self, event):
        if event.type()==QtCore.QEvent.WindowStateChange:
            if self.windowState() & QtCore.Qt.WindowFullScreen:
                self.setCursor(QtCore.Qt.BlankCursor)
            else:
                self.unsetCursor()
