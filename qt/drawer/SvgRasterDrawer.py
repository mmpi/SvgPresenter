from PyQt4 import QtCore, QtGui

class SvgRasterDrawer:
    def __init__(self, slide, log):
        self.slide = slide
    def image(self, size):
        return QtGui.QImage(self.slide.provideRasterImageWithResolution(size.width(), size.height()))
