from PyQt4 import QtCore
from PyQt4 import QtGui

from MovieWidget import MovieWidget

class SlideArea(QtGui.QLabel):
    resized = QtCore.pyqtSignal('float')

    def __init__(self, parent, presentation):
        QtGui.QLabel.__init__(self, parent)

        self.movieWidgets = []
        self.presentation = presentation

#         self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
#         self.setAlignment(Qt.AlignCenter)
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background, QtCore.Qt.black)
        self.setPalette(palette)
#         self.resize(1024,768)

    def showNewSlide(self):
        for w in self.movieWidgets:
            w.stop()
            self.resized.disconnect(w.updateGeometry)
            w.close()
        self.movieWidgets = []
        self.setLabelPixmap()

    def setLabelPixmap(self):
        original = self.presentation.getCurrentPixmap()
        if not original is None:
            size = QtCore.QSizeF(original.size())
            size.scale(QtCore.QSizeF(self.size()), QtCore.Qt.KeepAspectRatio)
            self.factor = size.width()/original.size().width()
    #         print self.factor 
            self.setPixmap(original.scaled(self.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        else:
            self.setPixmap(QtGui.QPixmap())
            
    def resizeEvent(self, event):
        self.setLabelPixmap()
        self.resized.emit(self.factor)
#         print self.pos().x(),self.pos().y()

    def nativeResolution(self):
        original = self.presentation.getCurrentPixmap()
        if original is None:
            return QtCore.QSize(0,0)
        else:
            return original.size()
    
    def startMovie(self):
        movieData = self.presentation.getCurrentMovieData()
        if movieData is None:
            return
        mediaPlayer = self.presentation.createMediaPlayer()
        widget = MovieWidget(self, movieData, mediaPlayer)
        widget.updateGeometry(self.factor)
        widget.start()
        self.resized.connect(widget.updateGeometry)
        self.movieWidgets.append(widget)
