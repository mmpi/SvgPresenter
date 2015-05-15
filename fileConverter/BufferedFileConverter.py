import sys
from buffer.FileBuffer import FileBuffer

class BufferedFileConverter:
    # to be overloaded:
    FileNameExtension = ""
    def convert(self, fromPath, toPath, *args, **kwargs):
        return True
    
    def __init__(self, fromBuffer, toBuffer):
        self.fromBuffer = fromBuffer
        self.toBuffer = toBuffer
    
    def convertForHash(self, hash, *args, **kwargs):
        toPath = self.toBuffer.useFileWithHash(hash)
        if toPath is None:
            fromPath = self.fromBuffer.useFileWithHash(hash)
            if fromPath is None:
                print "Did not find hash %s in file buffer %s."%(hash, self.fromBuffer.path)
                sys.exit(1)
            toPath = self.toBuffer.registerAndUseFileWithHash(hash, self.FileNameExtension)
            if not self.convert(fromPath, toPath, *args, **kwargs):
                return None
        return toPath

#     def getResultingPathFromHash(self, data):
#         return self.buffer.usePathOfHash(hash)
