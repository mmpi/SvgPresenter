from FileBuffer import FileBuffer

class BufferedFileFilter:
    # to be overloaded:
    FileNameExtension = ""
    def createFileFromData(self, path, data):
        return True
    
    def __init__(self, buffer):
        self.buffer = buffer
    
    def filterData(self, data, *args, **kwargs):
        hash = FileBuffer.hashFromData(data)
        path = self.buffer.useFileWithHash(hash)
        if path is None:
            path = self.buffer.registerAndUseFileWithHash(hash, self.FileNameExtension)
            if not self.createFileFromData(path, data, *args, **kwargs):
                return None
        return path

    def getResultingPathFromHash(self, data):
        return self.buffer.usePathOfHash(hash)
