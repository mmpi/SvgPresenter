import os.path
import xml.etree.ElementTree as etree

from buffer.FileBuffer import FileBuffer
from svg.SvgData import SvgData
from svg.xmlNamespaces import NSS
from svg.DefsCollector import DefsCollector
from svg.SvgSlide import SvgSlide 

class SvgPresentation:
    @staticmethod
    def createBufferForSvgFile(path):
        baseFolderPath, svgFileName = os.path.split(path)
        baseFileName, extension = os.path.splitext(svgFileName)
        return FileBuffer(os.path.join(baseFolderPath, "SvgPresentation-"+baseFileName))
    
    def __init__(self, svgPath):
        self.buffer = SvgPresentation.createBufferForSvgFile(svgPath)
        self.slideBuffer = self.buffer.subBuffer("slides")

        print "Reading %s..."%svgPath
        file = open(svgPath, 'r')
        data = file.read()
        file.close()
        hash = FileBuffer.hashFromData(data)        
        print "Done."

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
    
    def cleanUp(self):
        self.buffer.cleanUp()
        
    def loadFromSvgData(self, data):
        self.reset()
        
        # parse data
        print "Parsing..."
#         try:
        tree = etree.ElementTree(etree.fromstring(data))
#         except:
#             print "Problem with lxml, falling back to standard library."
#             import xml.etree.ElementTree as etree
#             tree = etree.ElementTree(etree.fromstring(data))
        data = None
        print "Done."

        # look for layers and slides
        print "Looking for layers..."
        root = tree.getroot()
        layers = SvgData.extractAllLayers(root)
        print "%d layers found."%len(layers)

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
            SvgData.removeStyleAttribute(layer, "display:none")
            SvgData.removeStyleAttribute(layer, "display:inline")
            
#         tree.write(svgPath+"-debug.svg", encoding="UTF-8", xml_declaration=True)

        # create slides
        print "Creating slides..."
        for layerIndex, layer in enumerate(layers):
            # only loop over slides
            if SvgData.isBackground(layer):
                continue
            
#             print "."

            # new svg tree, because we will delete stuff!
            newSvgTree = etree.ElementTree(root.copy())
            newSvgRoot = newSvgTree.getroot()
            newLayers = SvgData.extractAllLayers(newSvgRoot)
            
            # scan for references
            defsCollector = DefsCollector(newSvgRoot)
            for newLayerIndex, newLayer in enumerate(newLayers):
                if (newLayerIndex==layerIndex) or SvgData.isBackground(newLayer):
                    defsCollector.addRecursively(newLayer)

            # delete unused defs
            newDefsList = root.findall("svg:defs", NSS)
            for defsElement in newDefsList:
                newSvgRoot.remove(defsElement)
                                    
            # delete unused layers
            for newLayerIndex, newLayer in enumerate(newLayers):
                if (newLayerIndex!=layerIndex) and not SvgData.isBackground(newLayer):
                    newSvgRoot.remove(newLayer)
            
            # add my defs
            newSvgRoot.insert(0, defsCollector.defs)

#             # convert tree into plain svg
#             hash, dummy = self.plainSvgFiles.hashAndOutput(svgTree.tostring(svgTree.getroot(), encoding="utf8"))
            
            # new slide into presentation structure
            slide = SvgSlide.createFromSvgRootElement(self.slideBuffer, newSvgRoot)
            self.slides.append(slide)
        print "Done."
        return True
    
    def loadFromXmlFile(self, path):
        self.reset()
        print "Loading buffered presentation data..."
        presentationTree = etree.parse(path)
        presentation = presentationTree.getroot()
        for e in presentation:
            slide = SvgSlide.createFromPresentationXmlElement(self.slideBuffer, e)
            self.slides.append(slide)
        print "Done."
        
    def saveToXmlFile(self, path):
        # create xml digest
        presentation = etree.Element("presentation")
        for slide in self.slides:
            presentation.append(slide.createPresentationXmlElement())
        presentationTree = etree.ElementTree(presentation)
        presentationTree.write(path, encoding="UTF-8", xml_declaration=True)

    def slide(self, index):
        return self.slides[index]
    
    def numberOfSlides(self):
        return len(self.slides)
