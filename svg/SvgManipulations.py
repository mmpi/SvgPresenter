import os.path
import shutil
from svg.XmlNamespaces import etree, NSS

MovieHrefKey = "{%s}moviehref"%NSS["svgpresenter"]
MoviePlayOnClick = "{%s}playonclick"%NSS["svgpresenter"]
MovieLoop = "{%s}loop"%NSS["svgpresenter"]
XLinkHref = "{%s}href"%NSS["xlink"]

def removeStyleAttribute(node, attribute):
    # read style attributes
    styleAttributeString = node.get("style")
    if styleAttributeString is None:
        styleAttributes = []
    else:
        styleAttributes = styleAttributeString.split(";")
    # show layer
    if attribute in styleAttributes:
        styleAttributes.remove(attribute)
    # write attributes
    if len(styleAttributes)>0:
        node.set("style", ";".join(styleAttributes))
    else:
        if "style" in node.attrib:
            del node.attrib["style"]

def extractAllLayers(root):
    layers = root.findall("svg:g[@inkscape:groupmode='layer']", NSS)
    if len(layers)==0:
        print "No inkscape layers fond. Looking for toplevel groups..."
        layers = root.findall("svg:g", NSS)
    layers.reverse()
    return layers

def isBackground(layer):
    BackgroundStartsWith = "background-slide"
    return layer.get("{%s}label"%NSS["inkscape"], "").lower().startswith(BackgroundStartsWith)

def collectReferences(root, elements):
    collector = DefsCollector(root)
    for e in elements:
        collector.addRecursively(e)
    return collector.defs

class DefsCollector:
    def __init__(self, root):
        self.root = root
        self.refids = {}
        self.defs = etree.Element("{%s}defs"%NSS["svg"])
    def addRecursively(self, e):
        self.checkAttributes(e.attrib)
        for child in e:
            self.addRecursively(child)
    def addRefid(self, id):
        if not id in self.refids:
            e = self.root.find(".//*[@id='%s']"%id)
            if e is None:
                print "Did not find id '%s'!"%id
            self.refids[id] = e
            if e is not None:
                self.defs.append(e)
                self.addRecursively(e)
    XLinkHref = "{%s}href"%NSS["xlink"]
    def checkAttributes(self, a):
        for key in a:
            v = a[key]
            if key==self.XLinkHref:
                if v[0]=="#":
                    self.addRefid(v[1:])
            else:
                if "url(#" in v:
                    sp = v.split("url(#")
                    for s in sp[1:]:
                        self.addRefid(s.split(")")[0])

def fetchAllMovies(path, substitutions):
    path = os.path.abspath(path)
    print path
    baseFolderPath, svgFileName = os.path.split(path)
    baseFileName, extension = os.path.splitext(svgFileName)
    
    # copy failsafe
    fsPathMask = os.path.join(baseFolderPath, baseFileName+"_failsafe%02d"+extension)
    count = 1
    while(os.path.isfile(fsPathMask%count)):
        count += 1
    print "Copy to %s..."%fsPathMask%count
    shutil.copy(path, fsPathMask%count)
    
    # load original
    print "Loading %s..."%svgFileName
    file = open(path, 'r')
    data = file.read()
    file.close()
    print "Parsing..." 
    tree = etree.ElementTree(etree.fromstring(data))
    data = None
#     tree = etree.parse(path)
    print "Done."
    root = tree.getroot()

    # look for movies
    movieElements = root.findall(".//*[@%s]"%MovieHrefKey, NSS)
    print "Found %d movies in %s."%(len(movieElements), svgFileName)
    
    # prepare substitutions
    l = len(substitutions)/2
    subst = dict(zip(substitutions[0:2*l-1:2],substitutions[1:2*l:2]))
        
    # copy movies and change paths    
    for movie in movieElements:
        mPath = movie.get(MovieHrefKey)
        print "| Movie Path: %s"%mPath
        if not mPath is None:
            head, tail = os.path.split(mPath)
            if head=="":
                print "| | Not moving anything!"
            else:
                toPath = os.path.join(baseFolderPath, tail)
                print "| | Copying movie to %s"%toPath
                try:
                    shutil.copy(mPath, toPath)
                except:
                    print "| | Failed!"
                print "| | Changing path to %s"%tail
                movie.set(MovieHrefKey, tail)
            if tail in subst:
                tail = subst[tail]
                print "| | Substituting to %s"%tail
                movie.set(MovieHrefKey, tail)
            print "| Done."
    print "Done."
    
    # saving svg file
    print "Saving as %s..."%path
    tree.write(path, encoding="UTF-8", xml_declaration=True)
    print "Done."
    
                
            
            
            
