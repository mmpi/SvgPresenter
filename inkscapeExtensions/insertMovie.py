#!/usr/bin/env python
import sys, tempfile, os.path, subprocess, shutil
from PyQt4 import QtCore
import inkex
import vlc
from svg.xmlNamespaces import NSS

try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree

class SvgPresenter(inkex.Effect):
    FrameFileName = "Frame.png"
    
    def __init__(self):
        inkex.Effect.__init__(self)

        self.OptionParser.add_option("-f", "--moviepath",
                        action="store", type="string",
                        dest="moviepath", default="",
                        help="Path of the movie file")

        self.OptionParser.add_option("-e", "--embedmovie",
                        action="store", type="inkbool",
                        dest="embedmovie", default=True,
                        help="Embed movie")

        self.OptionParser.add_option("-c", "--playonclick",
                        action="store", type="inkbool",
                        dest="playonclick", default=True,
                        help="Play on click")

        self.OptionParser.add_option("-l", "--loop",
                        action="store", type="inkbool",
                        dest="loop", default=True,
                        help="Loop movie")

        self.OptionParser.add_option("-s", "--stillimagefraction",
                        action="store", type="float",
                        dest="stillimagefraction", default=0.0,
                        help="Time of the still image (in sec)")
    
    def effect(self):
        # check if local file:
        if not os.path.isfile(self.options.moviepath):
#             raise Exception("\"%s\" is not a proper path!"%self.options.moviepath)
            sys.exit(1)
        
        # use libvlc to figure out movie dimensions
        instance = vlc.Instance(["--no-audio","--no-xlib"])
        mediaplayer = instance.media_player_new()
        media = instance.media_new(unicode(self.options.moviepath))
        mediaplayer.set_media(media)
        media.parse()
        duration = 1.0e-3*media.get_duration()
#         sys.stderr.write("duration: %.3f\n"%(duration))
        width, height = mediaplayer.video_get_size()
        
        
        # extract first image using ffmpeg
        tmpPath = tempfile.mkdtemp()
        framePath = os.path.join(tmpPath, self.FrameFileName)
        subprocess.check_output(["ffmpeg",
                                 "-ss", str(duration*0.01*self.options.stillimagefraction), 
                                 "-i", self.options.moviepath,
                                 "-vframes", "1",
                                 framePath]
                                , stderr=subprocess.STDOUT)
#         os.system("ffmpeg -i \"%s\" -ss 0 -vframes 1 \"%s\""%(self.options.moviepath, framePath))
        
        # load image to QByteArray
        firstFrameFile = QtCore.QFile(framePath)
        firstFrameFile.open(QtCore.QIODevice.ReadOnly)
        firstFrameArray = firstFrameFile.readAll()
        firstFrameFile.close()
        shutil.rmtree(tmpPath)
        
        # create image uri
        imageUri = QtCore.QByteArray("data:image/png;base64,")
        imageUri.append(firstFrameArray.toBase64())

        # create movie uri
        if self.options.embedmovie:
            # load movie to QByteArray
            movieFile = QtCore.QFile(self.options.moviepath)
            movieFile.open(QtCore.QIODevice.ReadOnly)
            movieFileArray = movieFile.readAll()
#             sys.stderr.write("%d\n"%(movieFileArray.size()))
            movieFile.close()
            
            # create image uri
            movieUri = QtCore.QByteArray("data:;base64,")
#             sys.stderr.write("%d\n"%(movieUri.size()))
            movieUri.append(movieFileArray.toBase64())
#             sys.stderr.write("%d\n"%(movieFileArray.toBase64().size()))
            movieUriData = movieUri.data()
#             sys.stderr.write("%d\n"%(movieUri.size()))
        else:
            movieUriData = self.options.moviepath
        
        # create image node
        def toString(b):
            if b: return "1"
            else: return "0"
        newNode = etree.Element("image", attrib={"width":str(width), "height":str(height),
                                                 "x":"0.0", "y":"0.0",
                                                 "{%s}href"%NSS["xlink"]:imageUri.data(),
                                                 "{%s}playonclick"%NSS["svgpresenter"]:toString(self.options.playonclick),
                                                 "{%s}loop"%NSS["svgpresenter"]:toString(self.options.loop),
                                                 "{%s}moviehref"%NSS["svgpresenter"]:movieUriData})
#         newNode = etree.Element("rect", attrib={"style": 
#                     "fill:#808080;fill-opacity:1", "width":str(width), "height":str(height), "x":"0.0", "y":"0.0"})
        self.current_layer.append(newNode)

if __name__ == "__main__":
    #sys.stderr.write("%s\n"%("; ".join(sys.argv)))
    e = SvgPresenter()
    e.affect()
   
