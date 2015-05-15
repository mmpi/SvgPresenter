import subprocess
from PyQt4 import QtCore
from PyQt4 import QtGui

from svg import BufferedFileFilter

def createPixmaps(svgLoader):
    print "Preparing slide pixmaps..."
    pngFiles = PlainSvgToPixmap(svgLoader.basePath)
    pixmaps = []
    for svgPath in svgLoader.svgPaths:
        pixmaps.append(pngFiles.output(svgPath))
    pngFiles.cleanUp()
    print "Done."
    return pixmaps

class PlainSvgToPixmap(BufferedFileFilter.BufferedFileFilter):
    FileNameExtension = ".png"
    def __init__(self, basePath, resolution="1024"):
        self.resolution = resolution
        BufferedFileFilter.BufferedFileFilter.__init__(self, basePath, "png-"+resolution)
    
    def createDataFromInput(self, svgPath):
        file = open(svgPath, 'rb')
        data = file.read()
        file.close()
        return data         
        
    def createFileFromData(self, path, svgPath, data):
        # use inkscape to convert slide to png
        print "."
        subprocess.check_output(["inkscape",
                                 "--without-gui",
                                 "--file="+svgPath,
                                 "--export-background-opacity=1.0",
                                 "--export-png="+path,])
        return True
    def outputFromFile(self, path):
        return QtGui.QPixmap(path)    
