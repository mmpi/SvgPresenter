from PyQt4 import QtCore
# from PyQt4 import QtGui

from BaseDisplay import BaseDisplay
from SlideArea import SlideArea
from BufferedSlideArea import BufferedSlideArea

class PresenterDisplay(BaseDisplay):
    def __init__(self, desktop, presentationController):
        BaseDisplay.__init__(self, desktop, presentationController)
        self.setWindowTitle("Presenter's display")
        
        self.slideArea = SlideArea(self, self.presentationController)
#         self.slideArea = BufferedSlideArea(self, self.presentationController)
        self.presentationController.slideChange.connect(self.slideArea.showNewSlide)

        self.setMinimumSize(640, 480)
        if self.desktop.screenCount()>1:
            self.resize(self.slideArea.preferredSize())
        else:
            self.resize(640, 480)
        self.putOnRightScreen()
    
    def resizeEvent(self, event):
        slideSize = self.slideArea.preferredSize(self.size())
        self.slideArea.setGeometry(0.5*(self.width()-slideSize.width()), 0.5*(self.height()-slideSize.height()), slideSize.width(), slideSize.height())

    def setFullScreen(self, bool):
        BaseDisplay.setFullScreen(self, bool and (self.desktop.screenCount()>1))
        
    def putOnRightScreen(self):
        self.putOnScreen(self.primaryScreenIndex())
        if self.desktop.screenCount()<=1:
            BaseDisplay.setFullScreen(self, False)

