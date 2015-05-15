from PyQt4 import QtCore, QtGui
import vlc.vlc as vlc

from log.Log import Log
from drawer.RasterImageDrawer import RasterImageDrawer
from drawer.SvgDrawer import SvgDrawer
from drawer.PdfDrawer import PdfDrawer

class PresentationController(QtCore.QObject):
    slideChange = QtCore.pyqtSignal()
    startMovie = QtCore.pyqtSignal()
    closeDown = QtCore.pyqtSignal()
               
    def __init__(self, presentation):
        QtCore.QObject.__init__(self)
        self.presentation = presentation
        self.slideSize = QtCore.QSize(presentation.width, presentation.height)

        self.log = Log()
        self.libvlc = vlc.Instance(["--no-audio","--no-xlib"])
        
        self.numSlides = self.presentation.numberOfSlides()
        self.slideDrawers = self.prepareSlideDrawers()
        self.setSlideIndex(0)

    def prepareSlideDrawers(self):
        self.log.write("Preparing slide drawers...")
        subLog = self.log.subLayer()
        slideDrawers = []
        Mode = "raster"
        DrawerGenerators = {"raster": lambda slide, log: RasterImageDrawer(slide.provideRasterImage(log)),
                            "svg":  lambda slide, log: SvgDrawer(slide.provideSvgFile(log)),
                            "pdf":  lambda slide, log: PdfDrawer(slide.providePdfFile(log)),}
        drawerGenerator = DrawerGenerators[Mode]
        for slide in self.presentation:
            slideDrawers.append(drawerGenerator(slide, subLog))
        self.log.write("Done.")
        return slideDrawers

    def drawSlide(self, painter):
        if self.slideIndex < self.numSlides:
            return self.slideDrawers[self.slideIndex](painter)

    def setSlideIndex(self, index):
        self.slideIndex = index
        if self.slideIndex < self.numSlides:
            self.slide = self.presentation.slide(self.slideIndex)
        self.movieOnSlide = -1
        self.currentMovieData = None
        self.slideChange.emit()

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
        