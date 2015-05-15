class Log:
    NewLayerPrefix = "| "
    def __init__(self, prefix=""):
        self.prefix = prefix
    def subLayer(self):
        return Log(self.prefix+self.NewLayerPrefix)
    def write(self, message):
        print self.prefix + message 