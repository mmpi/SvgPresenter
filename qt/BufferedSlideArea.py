from PyQt4 import QtCore, QtGui

from PixmapBuffer import PixmapBuffer
from movie.MovieWidget import MovieWidget

class BufferedSlideArea(QtGui.QLabel):
    resized = QtCore.pyqtSignal('float')

    def __init__(self, parent, presentationController):
        QtGui.QLabel.__init__(self, parent)
        self.presentationController = presentationController

        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background, QtCore.Qt.black)
        self.setPalette(palette)

        self.visible = True
        self.movieWidgets = []
        self.pixmapBuffer = PixmapBuffer(self.presentationController)
        self.pixmapBuffer.currentPixmapUpdated.connect(self.updatePixmap)
        self.pixmapBuffer.initialRefill()
        
    def toggleVisible(self):
        self.visible = not self.visible
        if not self.visible:
            self.closeDownMovies()
        self.updatePixmap()
         
    def showNewSlide(self, index):
        self.closeDownMovies()
        self.updatePixmap()

    def preferredSize(self, maxSize=None):
        if maxSize is None:
            return QtCore.QSize(self.pixmapBuffer.originalSize)
        else:
            scaledSize = QtCore.QSize(self.pixmapBuffer.originalSize)
            scaledSize.scale(maxSize, QtCore.Qt.KeepAspectRatio)
            return scaledSize

    def updatePixmap(self):
        if self.visible:
            pixmapSize = self.preferredSize(self.size())
            pixmap = self.pixmapBuffer.currentPixmap()
            if not pixmap is None:
                if pixmapSize==pixmap.size():
                    self.setPixmap(pixmap)
                else:
                    self.setPixmap(pixmap.scaled(pixmapSize, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
            else:
                self.setPixmap(QtGui.QPixmap())
            self.factor = 1.0*self.size().width()/self.pixmapBuffer.originalSize.width()
        else:
            self.setPixmap(QtGui.QPixmap())
        
    def resizeEvent(self, event):
        self.updatePixmap()
        self.pixmapBuffer.refill(self.size())
        self.resized.emit(self.factor)

    def startMovie(self):
        if self.visible:
            widget = MovieWidget(self, self.presentationController.getCurrentMovieData())
            self.resized.connect(widget.updateGeometry)
            self.movieWidgets.append(widget)
            widget.updateGeometry(self.factor)
            widget.start()

    def closeDownMovies(self):
        for w in self.movieWidgets:
            w.stop()
            self.resized.disconnect(w.updateGeometry)
            w.close()
        self.movieWidgets = []
        