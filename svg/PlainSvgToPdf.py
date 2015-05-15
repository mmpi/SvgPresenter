import os.path, subprocess, shutil
from PyQt4 import QtCore
from PyQt4 import QtGui

from svg import BufferedFileFilter

def createPdf(svgLoader):
    toPdf = SvgToPdf(svgLoader)
    toPdf.go()
    toPdf.cleanUp()

class SvgToPdf(BufferedFileFilter.BufferedFileFilter):
    FileNameExtension = ".pdf"
    def __init__(self, svgLoader):
        self.svgLoader = svgLoader
        self.svgPath = self.svgLoader.svgPath
        BufferedFileFilter.BufferedFileFilter.__init__(self, self.svgLoader.basePath, ".")
    def createDataFromInput(self, svgPath):
        file = open(svgPath, 'rb')
        data = file.read()
        file.close()
        return data         
    def createFileFromData(self, path, svgPath, data):
        print "Preparing slide pdfs..."
        pdfFiles = PlainSvgToPdf(self.basePath)
        pdfPaths = []
        for svgPath in self.svgLoader.svgPaths:
            pdfPaths.append(pdfFiles.output(svgPath))
        print "Done."
        pdfFiles.cleanUp()
        print "Concatenating slide pdfs..."
        subprocess.check_output(["pdftk"] + pdfPaths + ["cat", "output", path])
        print "Done."
        return True 
    def outputFromFile(self, path):
        svgBasePath, ext = os.path.splitext(self.svgPath)
        shutil.copy(path, svgBasePath+".pdf")
    def go(self):
        self.output(self.svgPath)


class PlainSvgToPdf(BufferedFileFilter.BufferedFileFilter):
    FileNameExtension = ".pdf"
    def __init__(self, basePath):
        BufferedFileFilter.BufferedFileFilter.__init__(self, basePath, "pdf")
    
    def createDataFromInput(self, svgPath):
        file = open(svgPath, 'rb')
        data = file.read()
        file.close()
        return data         
        
    def createFileFromData(self, path, svgPath, data):
        # use inkscape to convert slide to pdf
        print "."
        subprocess.check_output(["inkscape",
                                 "--without-gui",
                                 "--file="+svgPath,
                                 "--export-text-to-path",
                                 "--export-pdf="+path,])
        return True
    def outputFromFile(self, path):
        return path    
    