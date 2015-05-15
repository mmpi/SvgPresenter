from PyQt4 import QtCore, QtGui

class RasterImageDrawer:
    def __init__(self, fileName):
        self.pixmap = QtGui.QPixmap(fileName)
    def __call__(self, painter):
        painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
        painter.drawPixmap(painter.window(), self.pixmap)
