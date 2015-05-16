from PyQt4 import QtCore, QtGui

# until now somewhat inconsistent...
class SvgRasterDrawer:
    def __init__(self, slide, log):
        self.slide = slide
        self.pixmapOfOriginalSize = QtGui.QPixmap(slide.provideRasterImage(log))
    def __call__(self, painter):
        painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
        painter.drawPixmap(painter.window(), self.pixmapOfOriginalSize)
    def image(self, size):
        return QtGui.QImage(self.slide.provideRasterImageWithResolution(size.width(), size.height()))
