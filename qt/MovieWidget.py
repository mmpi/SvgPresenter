# from PyQt4 import QtCore
from PyQt4 import QtGui
import vlc.vlc as vlc

class MovieWidget(QtGui.QWidget):
    def __init__(self, parent, movieData, mediaPlayer):
        QtGui.QWidget.__init__(self, parent)
        
#         palette = QtGui.QPalette()
#         palette.setColor(QtGui.QPalette.Background, QtCore.Qt.red)
#         self.setPalette(palette)

        self.data = movieData
        self.player = mediaPlayer
        self.player.set_media(self.data["media"])
        self.player.video_set_aspect_ratio("%d:%d"%(self.data["width"],self.data["height"]))
        self.eventManager = self.player.event_manager()
        self.eventManager.event_attach(vlc.EventType.MediaPlayerEndReached, self.stopped, 1)
        self.eventManager.event_attach(vlc.EventType.MediaPlayerStopped, self.stopped, 1)

        self.show()
        self.player.set_xwindow(self.winId())

    def start(self):
        self.player.play()
#         while not self.player.is_playing():
#             pass
#         self.player.pause()

    def stop(self):
        self.player.stop()
        
    def updateGeometry(self, factor):
        self.setGeometry(factor*self.data["x"], factor*self.data["y"], factor*self.data["width"], factor*self.data["height"])

    @vlc.callbackmethod
    def stopped(self, *args, **kwargs):
#         print "Stopped: ", self.data["path"]
#         self.close()
        pass