import subprocess

from log.Log import Log
from svg.XmlNamespaces import etree, NSS
import svg.SvgManipulations as SvgManipulations
from buffer.FileBuffer import FileBuffer

from fileConverter.BufferedSvgToPng import BufferedSvgToPng
from fileConverter.BufferedSvgToPdf import BufferedSvgToPdf
from fileConverter.BufferedPdfToSvg import BufferedPdfToSvg

class SvgSlide:
    @staticmethod
    def createFromSvgRootElement(log, buffer, svgRoot):
        slide = SvgSlide(log, buffer)

        data = etree.tostring(svgRoot, encoding='ascii')
        slide.hash = FileBuffer.hashFromData(data)
#         self.rawSvgFile = SvgWriter(self.rawBuffer).write(data) # such that the presentation xml file can be smaller
        data = None
        
        xmlPath = slide.xmlBuffer.useFileWithHash(slide.hash)
        if xmlPath is None:
            slide.loadFromSvgRootElement(svgRoot)
            xmlPath = slide.xmlBuffer.registerAndUseFileWithHash(slide.hash, ".xml")
            slide.saveSlideXmlData(xmlPath)
        else:
            slide.loadSlideXmlData(xmlPath)

        return slide
        
    @staticmethod
    def createFromPresentationXmlElement(buffer, element):
        slide = SvgSlide(Log(), buffer)
        slide.hash = element.attrib["hash"]
        xmlpath =  slide.xmlBuffer.useFileWithHash(slide.hash)
        if xmlpath is None:
            return None
        else:
            slide.loadSlideXmlData(xmlpath)
            return slide
    
    def createPresentationXmlElement(self):
        slide = etree.Element("slide")
        slide.attrib["hash"] = self.hash
        return slide

    def __init__(self, log, buffer):
        self.log = log
        
        # buffers
        self.buffer = buffer
        self.rawSvgBuffer = self.buffer.subBuffer("rawSvg")
        self.xmlBuffer = self.buffer.subBuffer("xml")
        self.pdfBuffer = self.buffer.subBuffer("pdf")
        self.svgBuffer = self.buffer.subBuffer("svg")
        self.pngBuffer = self.buffer.subBuffer("png")

        # converters
        self.rawSvgToPdf = BufferedSvgToPdf(self.rawSvgBuffer, self.pdfBuffer)
        self.pdfToSvg = BufferedPdfToSvg(self.pdfBuffer, self.svgBuffer)
        self.svgToPng = BufferedSvgToPng(self.rawSvgBuffer, self.pngBuffer)
        
        # the following will be set by the static factory functions
        self.hash = None
        self.movieData = []
    
    def loadFromSvgRootElement(self, svgRoot):
        self.log.write("Loading slide from svg data...")
        subLog = self.log.subLayer()
        
        # TODO: this should actually be done by a SvgSlideLayer class
        svgPath = self.rawSvgBuffer.registerAndUseFileWithHash(self.hash, ".svg")
        etree.ElementTree(svgRoot).write(svgPath, encoding="UTF-8", xml_declaration=True)
        
        # movies
        self.movieData = []
        movieElements = svgRoot.findall(".//*[@%s]"%SvgManipulations.MovieHrefKey, NSS)
        if len(movieElements)>0:
            subLog.write("Querying movie positions and sizes...")
            output = subprocess.check_output(["inkscape",
                                              "--without-gui",
                                              "--file="+svgPath,
                                              "--query-all",])
            
            PositionAndSizeFields = ["x","y","width","height"]
            lines = output.split()
            objects = {}
            for line in lines:
                fields = line.split(",")
                id = fields[0]
                objects[id] = {}
                for i, k in enumerate(PositionAndSizeFields):
                    objects[id][k] = fields[i+1]
            
            for movie in movieElements:
                d = {}
                d["path"] = movie.get(SvgManipulations.MovieHrefKey)
                d["playonclick"] = movie.get(SvgManipulations.MoviePlayOnClick, "1") == "1"
                d["loop"] = movie.get(SvgManipulations.MovieLoop, "0") == "1"
                d["image"] = movie.get(SvgManipulations.XLinkHref)
                id = movie.get("id")
                for key in PositionAndSizeFields:
                    d[key] = float(objects[id][key])
                self.movieData.append(d)
#         self.log.write("Done.")
       
    def saveSlideXmlData(self, xmlPath):
        slide = etree.Element("slide")
        etree.SubElement(slide, "static")
        for md in self.movieData:
            m = etree.SubElement(slide, "movie")
            for key in md:
                m.attrib[key] = str(md[key])
        tree = etree.ElementTree(slide)
        tree.write(xmlPath, encoding="UTF-8", xml_declaration=True)
     
    def loadSlideXmlData(self, xmlPath):
        self.movieData = []

        tree = etree.parse(xmlPath)
        slide = tree.getroot()
        for e in slide:
            if e.tag == "movie":
                d = {}
                for key in ["path", "image"]:
                    d[key] = e.attrib[key]
                for key in ["x", "y", "width", "height"]:
                    d[key] = float(e.attrib[key])
                for key in ["playonclick", "loop"]:
                    d[key] = e.attrib[key] == "True"
                self.movieData.append(d)
                
    def providePdfFile(self, log=None):
        return self.rawSvgToPdf.convertForHash(self.hash, log)

    def provideSvgFile(self, log=None):
        self.rawSvgToPdf.convertForHash(self.hash, log)
        return self.pdfToSvg.convertForHash(self.hash, log)

    def provideRasterImage(self, log=None):
        return self.svgToPng.convertForHash(self.hash, log)
    
    def numberOfMovies(self):
        return len(self.movieData)

    def dataForMovie(self, movieIndex):
        return self.movieData[movieIndex]
    