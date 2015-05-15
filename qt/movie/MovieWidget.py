from PyQt4 import QtCore, QtGui
import vlc.vlc as vlc

from MovieData import MovieData

class MovieWidget(QtGui.QLabel):
    def __init__(self, parent, movieData):
        QtGui.QWidget.__init__(self, parent)
        
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background, QtCore.Qt.black)
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        
        self.data = movieData
        self.player = MovieData.libvlc.media_player_new()

        self.player.set_media(self.data.media)
        self.player.video_set_aspect_ratio(self.data.aspectRatio())
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
        self.setGeometry(self.data.scaledRectangle(factor))
        self.setPixmap(self.data.pixmap.scaled(self.size(), QtCore.Qt.KeepAspectRatio))

    @vlc.callbackmethod
    def stopped(self, *args, **kwargs):
#         print "Stopped: ", self.data["path"]
#         self.close()
#         print "trying to release player..."
        self.player.release()
        pass