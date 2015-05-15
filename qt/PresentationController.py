from PyQt4 import QtCore
import vlc
# from svg.PlainSvgToPixmap import createPixmaps

class PresentationController(QtCore.QObject):
    slideChange = QtCore.pyqtSignal()
    startMovie = QtCore.pyqtSignal()
    closeDown = QtCore.pyqtSignal()
               
    def __init__(self, svgLoader):
        QtCore.QObject.__init__(self)
        self.svgLoader = svgLoader
        self.pixmaps = createPixmaps(self.svgLoader)
        self.movieData = self.svgLoader.movieData
        self.numSlides = len(self.pixmaps)
        
        self.libvlc = vlc.Instance(["--no-audio","--no-xlib"])
        self.slideIndex = 0
        self.movieOnSlide = -1
        self.currentMovie = None

    def getCurrentPixmap(self):
        if self.slideIndex == self.numSlides:
            return None
        else:
            return self.pixmaps[self.slideIndex]

    def getCurrentMovieData(self):
        return self.currentMovie
    
    def createMediaPlayer(self):
        return self.libvlc.media_player_new()
    
    def first(self):
        self.slideIndex = 0
        self.movieOnSlide = -1
        self.currentMovie = None
        self.slideChange.emit()

    def last(self):
        self.slideIndex = self.numSlides-1
        self.movieOnSlide = -1
        self.currentMovie = None
        self.slideChange.emit()

    def forward(self):
        if self.slideIndex < self.numSlides:
            # not yet all movies shown?
            self.movieOnSlide += 1
            if self.movieOnSlide<len(self.movieData[self.slideIndex]):
                self.currentMovie = self.movieData[self.slideIndex][self.movieOnSlide]
                
                media = self.libvlc.media_new(unicode(self.currentMovie["path"]))
                if self.currentMovie["loop"]:
                    media.add_option("input-repeat=-1") # repeat
                self.currentMovie["media"] = media
    
                self.startMovie.emit()
            else:
                self.slideIndex += 1
                self.movieOnSlide = -1
                self.currentMovie = None
                self.slideChange.emit()
        
    def backward(self):
        self.slideIndex -= 1
        self.movieOnSlide = -1
        if self.slideIndex < 0:
            self.slideIndex = 0
        self.currentMovie = None
        self.slideChange.emit()
                
    def close(self):
        self.closeDown.emit()