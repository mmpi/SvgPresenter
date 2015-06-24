from PyQt4 import QtCore, QtGui, QtSvg
from DrawingFunctions import *

class SvgDrawer:
    def __init__(self, pagecolor, fileName):
        self.pageColor = svgColorToQtColor(pagecolor)
        self.renderer = QtSvg.QSvgRenderer(fileName)
    def __call__(self, painter):
        painter.setBackground(self.pageColor)
        painter.eraseRect(painter.window())
        self.renderer.render(painter)
    def image(self, size):
        img = QtGui.QImage(size, QtGui.QImage.Format_RGB32)
        img.fill(self.pageColor)
        painter = QtGui.QPainter()
        painter.begin(img)
        self(painter)
        painter.end()
        return img
