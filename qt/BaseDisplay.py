from PyQt4 import QtCore
from PyQt4 import QtGui


class BaseDisplay(QtGui.QMainWindow):
    def __init__(self, presentationController):
        QtGui.QMainWindow.__init__(self)
        
        self.presentationController = presentationController
        self.presentationController.closeDown.connect(self.close)

        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background, QtCore.Qt.black)
        self.setPalette(palette)
        self.setMinimumSize(640, 480)
#         self.setFocus()
    
    def keyPressEvent(self, event):
        if(event.key() in [QtCore.Qt.Key_Right, QtCore.Qt.Key_Down, QtCore.Qt.Key_PageDown]):
            self.presentationController.forward()
        elif(event.key() in [QtCore.Qt.Key_Left, QtCore.Qt.Key_Up, QtCore.Qt.Key_PageUp]):
            self.presentationController.backward()
        elif(event.key() in [QtCore.Qt.Key_Home]):
            self.presentationController.first()
        elif(event.key() in [QtCore.Qt.Key_End]):
            self.presentationController.last()
        elif(event.key()==QtCore.Qt.Key_Escape):
            self.presentationController.close()
        else:
#             print event.key()
            return QtGui.QMainWindow.keyPressEvent(self, event)