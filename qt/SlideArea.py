from PyQt4 import QtCore
from PyQt4 import QtGui

from movie.MovieWidget import MovieWidget

class SlideArea(QtGui.QWidget):
    resized = QtCore.pyqtSignal('float')

    def __init__(self, parent, presentationController):
        QtGui.QWidget.__init__(self, parent)

        self.movieWidgets = []
        self.presentationController = presentationController
        self.slideSize = QtCore.QSize(self.presentationController.slideSize)

#         self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
#         self.setAlignment(Qt.AlignCenter)
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background, QtCore.Qt.black)
        self.setPalette(palette)

    def showNewSlide(self):
        for w in self.movieWidgets:
            w.stop()
            self.resized.disconnect(w.updateGeometry)
            w.close()
        self.movieWidgets = []
        self.update()

    def preferredSize(self, maxSize=None):
        if maxSize is None:
            return QtCore.QSize(self.slideSize)
        else:
            scaledSize = QtCore.QSize(self.slideSize)
            scaledSize.scale(maxSize, QtCore.Qt.KeepAspectRatio)
            return scaledSize

    def resizeEvent(self, event):
        self.factor = 1.0*self.size().width()/self.slideSize.width()
        self.update()
        self.resized.emit(self.factor)

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        self.presentationController.drawSlide(painter, self.presentationController.slideIndex)
        painter.end()

    def startMovie(self):
        widget = MovieWidget(self, self.presentationController.getCurrentMovieData())
        self.resized.connect(widget.updateGeometry)
        self.movieWidgets.append(widget)
        widget.updateGeometry(self.factor)
        widget.start()
