from svg.XmlNamespaces import etree, NSS

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
