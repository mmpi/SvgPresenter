import os.path
import subprocess

from log.Log import Log
from buffer.FileBuffer import FileBuffer
from svg.XmlNamespaces import etree, NSS
import svg.SvgManipulations as SvgManipulations
from svg.SvgSlide import SvgSlide 

class SvgPresentation:
    @staticmethod
    def createBufferForSvgFile(path):
        baseFolderPath, svgFileName = os.path.split(path)
        baseFileName, extension = os.path.splitext(svgFileName)
        return FileBuffer(os.path.join(baseFolderPath, "SvgPresentation-"+baseFileName))
    
    def __init__(self, svgPath):
        self.log = Log()
        self.svgPath = svgPath
        self.buffer = SvgPresentation.createBufferForSvgFile(svgPath)
        self.slideBuffer = self.buffer.subBuffer("slides")
        
        self.log.write("Reading %s..."%svgPath)
        file = open(svgPath, 'r')
        data = file.read()
        file.close()
        hash = FileBuffer.hashFromData(data)        
#         self.log.write("Done.")

        xmlPath = self.buffer.useFileWithHash(hash)
        if xmlPath is None:
            if not self.loadFromSvgData(data):
                return
            data = None
            xmlPath = self.buffer.registerAndUseFileWithHash(hash, ".xml")
            self.saveToXmlFile(xmlPath)
        else:
            data = None
            self.loadFromXmlFile(xmlPath)

    def reset(self):
        self.slides = []
        
    def __iter__(self):
        return self.slides.__iter__()
    
    def cleanUp(self):
        self.buffer.cleanUp()
        
    def loadFromSvgData(self, data):
        self.reset()
        
        # parse data
        self.log.write("Parsing...")
#         try:
        tree = etree.ElementTree(etree.fromstring(data))
#         except:
#             print "Problem with lxml, falling back to standard library."
#             import xml.etree.ElementTree as etree
#             tree = etree.ElementTree(etree.fromstring(data))
        data = None
        root = tree.getroot()
#         self.log.write("Done.")

        # check dimensions
        self.width = float(root.get("width"))
        self.height = float(root.get("height"))

        # look for layers and slides
        self.log.write("Looking for layers...")
        layers = SvgManipulations.extractAllLayers(root)
        self.log.write("%d layers found."%len(layers))

        # remove unneeded data (for a higher probability of hashs being equal)
        CopyKeys = ["id", "pagecolor", "{%s}pageopacity"%NSS["inkscape"]]
        sodipodis = root.findall("sodipodi:namedview", NSS)
        for s in sodipodis:
            a = {}
            for key in CopyKeys:
                a[key] = s.attrib[key]
            s.attrib = a

        # show all layers
        for layer in layers:
            SvgManipulations.removeStyleAttribute(layer, "display:none")
            SvgManipulations.removeStyleAttribute(layer, "display:inline")
            
#         tree.write(svgPath+"-debug.svg", encoding="UTF-8", xml_declaration=True)

        # create slides
        self.log.write("Creating slides...")
        for layerIndex, layer in enumerate(layers):
            # only loop over slides
            if SvgManipulations.isBackground(layer):
                continue
            
#             print "."

            # xmlNamespacesnew svg tree, because we will delete stuff!
            newSvgTree = etree.ElementTree(root.copy())
            newSvgRoot = newSvgTree.getroot()
            newLayers = SvgManipulations.extractAllLayers(newSvgRoot)
            
            # scan for references
            defsCollector = SvgManipulations.DefsCollector(newSvgRoot)
            for newLayerIndex, newLayer in enumerate(newLayers):
                if (newLayerIndex==layerIndex) or SvgManipulations.isBackground(newLayer):
                    defsCollector.addRecursively(newLayer)

            # delete unused RasterImagedefs
            newDefsList = root.findall("svg:defs", NSS)
            for defsElement in newDefsList:
                newSvgRoot.remove(defsElement)
                                    
            # delete unused layers
            for newLayerIndex, newLayer in enumerate(newLayers):
                if (newLayerIndex!=layerIndex) and not SvgManipulations.isBackground(newLayer):
                    newSvgRoot.remove(newLayer)
            
            # add my defs
            newSvgRoot.insert(0, defsCollector.defs)

#             # convert tree into plain svg
#             hash, dummy = self.plainSvgFiles.hashAndOutput(svgTree.tostring(svgTree.getroot(), encoding="utf8"))
            
            # new slide into presentation structure
            slide = SvgSlide.createFromSvgRootElement(self.log.subLayer(), self.slideBuffer, newSvgRoot)
            self.slides.append(slide)
        self.log.write("Done.")
        return True
    
    def loadFromXmlFile(self, path):
        self.reset()
        print "Loading buffered presentation data..."
        presentationTree = etree.parse(path)
        presentation = presentationTree.getroot()
        self.width = float(presentation.get("width"))
        self.height = float(presentation.get("height"))
        for e in presentation:
            slide = SvgSlide.createFromPresentationXmlElement(self.slideBuffer, e)
            self.slides.append(slide)
        print "Done."
        
    def saveToXmlFile(self, path):
        # create xml digest
        presentation = etree.Element("presentation")
        presentation.set("width", str(self.width))
        presentation.set("height", str(self.height))
        for slide in self.slides:
            presentation.append(slide.createPresentationXmlElement())
        presentationTree = etree.ElementTree(presentation)
        presentationTree.write(path, encoding="UTF-8", xml_declaration=True)

    def slide(self, index):
        return self.slides[index]
    
    def numberOfSlides(self):
        return len(self.slides)
    
    def exportAsPdf(self, pdfPath=None):
        if pdfPath is None:
            basePath, extension = os.path.splitext(self.svgPath)
            pdfPath = basePath + ".pdf"
            
        self.log.write("Exporting presentation as %s..."%pdfPath)
        subLog = self.log.subLayer()
        
        slidePdfPaths = []
        for slide in self.slides:
            slidePdfPaths.append(slide.providePdfFile(subLog))
            
        subLog.write("Concatenating...")
        subprocess.check_output(["pdftk"] + slidePdfPaths + ["cat", "output", pdfPath])
        
        self.log.write("Done.")        
        return pdfPath
