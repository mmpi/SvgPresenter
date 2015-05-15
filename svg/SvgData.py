from xmlNamespaces import NSS

class SvgData:
    @staticmethod
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

    @staticmethod
    def extractAllLayers(root):
        layers = root.findall("svg:g[@inkscape:groupmode='layer']", NSS)
        if len(layers)==0:
            print "No inkscape layers fond. Looking for toplevel groups..."
            layers = root.findall("svg:g", NSS)
        layers.reverse()
        return layers

    @staticmethod
    def isBackground(layer):
        BackgroundStartsWith = "background-slide"
        return layer.get("{%s}label"%NSS["inkscape"], "").lower().startswith(BackgroundStartsWith)
    