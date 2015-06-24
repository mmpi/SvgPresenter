import os.path
from PyQt4 import QtCore, QtGui
import vlc.vlc as vlc

class MovieData:
    libvlc = vlc.Instance(["--no-audio","--no-xlib"])

    def __init__(self, basePath, dict):
        self.basePath = basePath
        self.data = dict
        
        # load poster pixmap
        PngBase64 = "data:image/png;base64,"
        imageData = self.data["image"]
        if imageData.startswith(PngBase64):
            byteArray = QtCore.QByteArray.fromBase64(imageData[len(PngBase64):])
            self.pixmap = QtGui.QPixmap()
            self.pixmap.loadFromData(byteArray)
        
        # load medium
        path = self.data["path"]
        head, tail = os.path.split(path)
        if head=="":
            path = os.path.join(self.basePath, tail)
        self.media = self.libvlc.media_new(unicode(path))
        if self.data["loop"]:
            self.media.add_option("input-repeat=-1") # repeat
        
    def scaledRectangle(self, factor):
        return QtCore.QRect(factor*self.data["x"], factor*self.data["y"], factor*self.data["width"], factor*self.data["height"])
    
    def aspectRatio(self):
        return "%d:%d"%(self.data["width"],self.data["height"])