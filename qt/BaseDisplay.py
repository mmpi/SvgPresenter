from PyQt4 import QtCore
from PyQt4 import QtGui


class BaseDisplay(QtGui.QMainWindow):
    def __init__(self, desktop, presentationController):
        QtGui.QMainWindow.__init__(self)
        
        self.desktop = desktop
        self.desktop.screenCountChanged.connect(self.putOnRightScreen)
        self.exchangeScreens = False
        self.presentationController = presentationController
        self.presentationController.closeDown.connect(self.close)
        self.presentationController.changedFullScreen.connect(self.setFullScreen)
        self.presentationController.changedExchangeScreens.connect(self.setExchangeScreens)
        
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background, QtCore.Qt.black)
        self.setPalette(palette)
        self.setMinimumSize(640, 480)
#         self.setFocus()
    
    def keyPressEvent(self, event):
#         print "key"
#         print "0x%02x"%event.key(), "0x%02x"%event.modifiers()
        if event.key() in [QtCore.Qt.Key_Right, QtCore.Qt.Key_Down, QtCore.Qt.Key_PageDown]:
            self.presentationController.forward()
        elif event.key() in [QtCore.Qt.Key_Left, QtCore.Qt.Key_Up, QtCore.Qt.Key_PageUp]:
            self.presentationController.backward()
        elif event.key() in [QtCore.Qt.Key_Home]:
            self.presentationController.first()
        elif event.key() in [QtCore.Qt.Key_End]:
            self.presentationController.last()
        elif (event.modifiers(), event.key()) in [(QtCore.Qt.ControlModifier, QtCore.Qt.Key_Q),
                                                  (QtCore.Qt.AltModifier,     QtCore.Qt.Key_F4)]:
            self.presentationController.close()
        elif event.key()==QtCore.Qt.Key_B:
            self.presentationController.toggleAudience()
        elif event.key()==QtCore.Qt.Key_X:
            self.presentationController.toggleExchangeScreens()
        elif (event.modifiers(), event.key()) in [(QtCore.Qt.ShiftModifier, QtCore.Qt.Key_F5)]:
            self.presentationController.setFullScreen(True)
        elif event.key() in [QtCore.Qt.Key_Escape]:
            self.presentationController.setFullScreen(False)
        else:
            return QtGui.QMainWindow.keyPressEvent(self, event)
        
    def mouseDoubleClickEvent (self, event):
        self.setWindowState(self.windowState() ^ QtCore.Qt.WindowFullScreen)
        
    def setFullScreen(self, bool):
        if bool:
            self.setWindowState(self.windowState() | QtCore.Qt.WindowFullScreen)
        else:
            self.setWindowState(self.windowState() & ~QtCore.Qt.WindowFullScreen)

    def setExchangeScreens(self, exchangeScreens):
        self.exchangeScreens = exchangeScreens
        print "es:", self.exchangeScreens
        self.putOnRightScreen()

    def otherScreenIndex(self, index):
        if self.desktop.screenCount()>1:
            return 1-index
        else:
            return index

    def primaryScreenIndex(self):
#         if self.desktop.screenCount() not in [1,2]:
        print "%d screens."%self.desktop.screenCount()
        if self.desktop.screenCount()>1:
            if self.exchangeScreens:
                return self.otherScreenIndex(self.desktop.primaryScreen())
            else:
                return self.desktop.primaryScreen()
        elif self.desktop.screenCount()==1:
            return self.desktop.primaryScreen()
        else:
            return -1

    def putOnScreen(self, screenIndex):
        print self.windowTitle(), screenIndex
        fullscreen = self.windowState() & QtCore.Qt.WindowFullScreen
        if fullscreen:
            self.setWindowState(self.windowState() & ~QtCore.Qt.WindowFullScreen)
        screenRect = self.desktop.availableGeometry(screenIndex)
        x = screenRect.x() + 0.5*(screenRect.width()-self.frameGeometry().width())
        y = screenRect.y() + 0.5*(screenRect.height()-self.frameGeometry().height())
        self.move(x, y)
        if fullscreen:
            self.setWindowState(self.windowState() | QtCore.Qt.WindowFullScreen)
            
                
                        
#     def putOnRightScreen(self, size=None):
#         # dummy implementation
#         screen = -1
#         if size is None:
#             self.setGeometry(self.desktop.screenGeometry(screen))
#         else:
#             self.setGeometry(QtCore.QRect(self.desktop.availableGeometry(screen).topLeft(), size))
