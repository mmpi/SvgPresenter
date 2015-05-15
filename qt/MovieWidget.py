from PyQt4 import QtCore, QtGui
import vlc.vlc as vlc

class MovieWidget(QtGui.QLabel):
    def __init__(self, parent, movieData, mediaPlayer):
        QtGui.QWidget.__init__(self, parent)
        
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background, QtCore.Qt.black)
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        
        PngBase64 = "data:image/png;base64,"
        imageData = movieData["image"]
        if imageData.startswith(PngBase64):
            byteArray = QtCore.QByteArray.fromBase64(imageData[len(PngBase64):])
            self.pixmap = QtGui.QPixmap()
            self.pixmap.loadFromData(byteArray)

        self.data = movieData
        self.player = mediaPlayer
        self.player.set_media(self.data["media"])
        self.player.video_set_aspect_ratio("%d:%d"%(self.data["width"],self.data["height"]))
        self.eventManager = self.player.event_manager()
        self.eventManager.event_attach(vlc.EventType.MediaPlayerEndReached, self.stopped, 1)
        self.eventManager.event_attach(vlc.EventType.MediaPlayerStopped, self.stopped, 1)

        self.player.set_xwindow(self.winId())
        self.show()

    def start(self):
        self.player.play()
        pass

    def stop(self):
        self.player.stop()
        
    def updateGeometry(self, factor):
        self.setGeometry(factor*self.data["x"], factor*self.data["y"], factor*self.data["width"], factor*self.data["height"])
        self.setPixmap(self.pixmap.scaled(self.size(), QtCore.Qt.KeepAspectRatio))

    @vlc.callbackmethod
    def stopped(self, *args, **kwargs):
#         print "Stopped: ", self.data["path"]
#         self.close()
        pass