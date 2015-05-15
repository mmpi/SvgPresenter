import xml.etree.ElementTree as etree
from buffer.FileBuffer import FileBuffer
from svg.xmlNamespaces import NSS
from svg.SvgWriter import SvgWriter

class SvgSlide:
    @staticmethod
    def createFromSvgRootElement(buffer, svgRoot):
        slide = SvgSlide(buffer)

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
        slide = SvgSlide(buffer)
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

    def __init__(self, buffer):
        self.buffer = buffer
        self.svgBuffer = self.buffer.subBuffer("svg")
        self.xmlBuffer = self.buffer.subBuffer("xml")
        
    def loadFromSvgRootElement(self, svgRoot):
        print "Loading slide from svg data..."
        # TODO: this should actually be done by a SvgSlideLayer class
        svgPath = self.svgBuffer.registerAndUseFileWithHash(self.hash, ".svg")
        etree.ElementTree(svgRoot).write(svgPath, encoding="UTF-8", xml_declaration=True)
        
        # movies
        self.movieData = []
        MovieHrefKey = "{%s}moviehref"%NSS["svgpresenter"]
        MoviePlayOnClick = "{%s}playonclick"%NSS["svgpresenter"]
        MovieLoop = "{%s}loop"%NSS["svgpresenter"]
        movieElements = svgRoot.findall(".//*[@%s]"%MovieHrefKey, NSS)
        for movie in movieElements:
            d = {}
            d["path"] = movie.get(MovieHrefKey)
            d["playonclick"] = movie.get(MoviePlayOnClick, "1") == "1"
            d["loop"] = movie.get(MovieLoop, "0") == "0"
            d["x"] = float(movie.get("x"))
            d["y"] = float(movie.get("y"))
            d["width"] = float(movie.get("width"))
            d["height"] = float(movie.get("height"))
            self.movieData.append(d)

        
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
                for key in ["path"]:
                    d[key] = e.attrib[key]
                for key in ["x", "y", "width", "height"]:
                    d[key] = float(e.attrib[key])
                for key in ["playonclick", "loop"]:
                    d[key] = e.attrib[key] == "True"
                self.movieData.append(d)
                
     
    
    def pixmap(self):
        pass
    
    def plainSvgPath(self):
        # path of svg file without any flowed text and movies
        pass
    
    def movieData(self):
        pass
    