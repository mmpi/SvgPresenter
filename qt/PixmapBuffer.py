from PyQt4 import QtCore, QtGui

class DrawerThread(QtCore.QThread):
    pixmapUpdated = QtCore.pyqtSignal('int', 'QImage')
    
    def __init__(self, slideDrawers, imageSize, startwithIndex):
        QtCore.QThread.__init__(self)
        self.slideDrawers = slideDrawers
        self.numSlides = len(self.slideDrawers) 
        self.imageSize = imageSize
        self.startwithIndex = startwithIndex
        self.abort = False
        
    def run(self):
        for i in xrange(self.numSlides):
            if self.abort:
                break
            slideIndex = (i+self.startwithIndex) % self.numSlides
            image = self.slideDrawers[slideIndex].image(self.imageSize)
            self.pixmapUpdated.emit(slideIndex, image)       
        
    def stop(self):
        self.abort = True
        
class PixmapBuffer(QtCore.QObject):
    currentPixmapUpdated = QtCore.pyqtSignal()
    quitThread = QtCore.pyqtSignal()
    
    def __init__(self, presentationController):
        QtCore.QObject.__init__(self)
        self.presentationController = presentationController
        self.originalSize = QtCore.QSize(self.presentationController.slideSize)
        self.numSlides = self.presentationController.numSlides
        self.pixmaps = self.numSlides*[None]
        self.thread = None
        self.currentSize = None

    def currentPixmap(self):
        if self.presentationController.slideIndex<self.numSlides:
            return self.pixmaps[self.presentationController.slideIndex]
        
    def initialRefill(self):
        self.refill(self.originalSize)
#         self.wait()
        
    def refill(self, pixmapSize):
        print pixmapSize
        if pixmapSize!=self.currentSize:
            print "A"
            self.currentSize = pixmapSize
            if not self.thread is None:
                print "B"
                if self.thread.isRunning():
                    print "C"
                    self.quitThread.emit()
                    print "C1"
                    self.thread.wait()
                    print "D"
                    self.thread.pixmapUpdated.disconnect()
                    print "D1"
                    self.quitThread.disconnect()
                    print "E"
            self.thread = DrawerThread(self.presentationController.slideDrawers, pixmapSize, self.presentationController.slideIndex)
            print "F"
            self.quitThread.connect(self.thread.stop)
            print "G"
            self.thread.pixmapUpdated.connect(self.updatePixmap)
            print "H"
            self.thread.start()
            print "I"

        
    def wait(self):
        self.thread.wait()

    def updatePixmap(self, index, image):
        self.pixmaps[index] = QtGui.QPixmap.fromImage(image)
        print "PixmapBuffer.updatePixmap", index, self.presentationController.slideIndex
        if index == self.presentationController.slideIndex:
            print "emitting"
            self.currentPixmapUpdated.emit()
        
                
