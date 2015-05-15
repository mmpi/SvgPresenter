from PyQt4 import QtCore, QtGui
import vlc.vlc as vlc

from log.Log import Log
# from svg.PlainSvgToPixmap import createPixmaps

class PresentationController(QtCore.QObject):
    slideChange = QtCore.pyqtSignal()
    startMovie = QtCore.pyqtSignal()
    closeDown = QtCore.pyqtSignal()
               
    def __init__(self, presentation):
        QtCore.QObject.__init__(self)
        self.presentation = presentation

        self.log = Log()
        self.libvlc = vlc.Instance(["--no-audio","--no-xlib"])
        
        self.numSlides = self.presentation.numberOfSlides()
        self.pixmaps = self.preparePixmaps()
        self.setSlideIndex(0)

    def preparePixmaps(self):
        self.log.write("Preparing slide pixmaps...")
        subLog = self.log.subLayer()
        pixmaps = []
        for slide in self.presentation:
            pixmaps.append(QtGui.QPixmap(slide.provideRasterImage(subLog)))
        self.log.write("Done.")
        return pixmaps

    def setSlideIndex(self, index):
        self.slideIndex = index
        if self.slideIndex < self.numSlides:
            self.slide = self.presentation.slide(self.slideIndex)
        self.movieOnSlide = -1
        self.currentMovieData = None
        self.slideChange.emit()
    
    def getCurrentPixmap(self):
        if self.slideIndex < self.numSlides:
            return self.pixmaps[self.slideIndex]
        else:
            return None

    def getCurrentMovieData(self):
        return self.currentMovieData
    
    def createMediaPlayer(self):
        return self.libvlc.media_player_new()
    
    def first(self):
        self.setSlideIndex(0)

    def last(self):
        self.setSlideIndex(self.numSlides-1)

    def forward(self):
        if self.slideIndex < self.numSlides:
            # not yet all movies shown?
            self.movieOnSlide += 1
            if self.movieOnSlide < self.slide.numberOfMovies():
                self.currentMovieData = self.slide.dataForMovie(self.movieOnSlide)
                
                media = self.libvlc.media_new(unicode(self.currentMovieData["path"]))
                if self.currentMovieData["loop"]:
                    media.add_option("input-repeat=-1") # repeat
                self.currentMovieData["media"] = media
    
                self.startMovie.emit()
            else:
                self.setSlideIndex(self.slideIndex + 1)
        
    def backward(self):
        self.setSlideIndex(max(0, self.slideIndex - 1))
                
    def close(self):
        self.closeDown.emit()
        