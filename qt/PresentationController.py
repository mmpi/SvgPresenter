from PyQt4 import QtCore, QtGui

from log.Log import Log
from drawer.RasterImageDrawer import RasterImageDrawer
from drawer.SvgDrawer import SvgDrawer
from drawer.PdfDrawer import PdfDrawer
from movie.MovieData import MovieData

class PresentationController(QtCore.QObject):
    slideChange = QtCore.pyqtSignal()
    startMovie = QtCore.pyqtSignal()
    closeDown = QtCore.pyqtSignal()
               
    def __init__(self, presentation):
        QtCore.QObject.__init__(self)
        self.presentation = presentation
        self.slideSize = QtCore.QSize(presentation.width, presentation.height)

        self.log = Log()
        self.numSlides = self.presentation.numberOfSlides()
        self.slideDrawers = self.prepareSlideDrawers()
        self.movieData = self.prepareMovieData()
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

    def prepareMovieData(self):
        self.log.write("Preparing movie data...")
        movieDataForAllSlides = []
        for slide in self.presentation:
            movieDataForCurrentSlide = []
            for i in xrange(slide.numberOfMovies()):
                movieDataForCurrentSlide.append(MovieData(slide.dataForMovie(i)))
            movieDataForAllSlides.append(movieDataForCurrentSlide)
        self.log.write("Done.")
        return movieDataForAllSlides

    def drawSlide(self, painter):
        if self.slideIndex < self.numSlides:
            return self.slideDrawers[self.slideIndex](painter)

    def setSlideIndex(self, index):
        self.slideIndex = index
        if self.slideIndex < self.numSlides:
            self.slide = self.presentation.slide(self.slideIndex)
            self.currentMovieData = self.movieData[index]
        self.movieOnSlide = -1
        self.slideChange.emit()

    def getCurrentMovieData(self):
        return self.currentMovieData[self.movieOnSlide]
    
    def first(self):
        self.setSlideIndex(0)

    def last(self):
        self.setSlideIndex(self.numSlides-1)

    def forward(self):
        if self.slideIndex < self.numSlides:
            # not yet all movies shown?
            self.movieOnSlide += 1
            if self.movieOnSlide < self.slide.numberOfMovies():
                self.startMovie.emit()
            else:
                self.setSlideIndex(self.slideIndex + 1)
        
    def backward(self):
        self.setSlideIndex(max(0, self.slideIndex - 1))
                
    def close(self):
        self.closeDown.emit()
        