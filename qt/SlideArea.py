from PyQt4 import QtCore
from PyQt4 import QtGui

from MovieWidget import MovieWidget

class SlideArea(QtGui.QLabel):
    resized = QtCore.pyqtSignal('float')

    def __init__(self, parent, presentationController):
        QtGui.QLabel.__init__(self, parent)

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
            return QtCore.QSize(self.presentationController.slideSize)
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
        self.presentationController.drawSlide(painter)
        painter.end()

    def startMovie(self):
        movieData = self.presentationController.getCurrentMovieData()
        if movieData is None:
            return
        mediaPlayer = self.presentationController.createMediaPlayer()
        widget = MovieWidget(self, movieData, mediaPlayer)
        widget.updateGeometry(self.factor)
        self.resized.connect(widget.updateGeometry)
        self.movieWidgets.append(widget)
        widget.start()
