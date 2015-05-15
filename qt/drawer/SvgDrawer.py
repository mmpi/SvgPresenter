from PyQt4 import QtCore, QtGui, QtSvg

class SvgDrawer:
    def __init__(self, fileName):
        self.renderer = QtSvg.QSvgRenderer(fileName)
    def __call__(self, painter):
        self.renderer.render(painter)
