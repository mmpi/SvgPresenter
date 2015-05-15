import xml.etree.ElementTree as etree

from xmlNamespaces import NSS

class DefsCollector:
    @staticmethod
    def collectReferences(root, elements):
        collector = DefsCollector(root)
        for e in elements:
            collector.addRecursively(e)
        return collector.defs
    
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
            
