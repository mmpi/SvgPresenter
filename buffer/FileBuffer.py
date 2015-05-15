import os
import os.path
import hashlib, base64

class FileBuffer:
    def __init__(self, path):
        self.path = path
        if not os.path.isdir(self.path):
            os.makedirs(self.path)
        # load hash keys from filenames
        self.existingFiles = {}
        for entry in os.listdir(self.path):
            subpath = os.path.join(self.path, entry)
            if os.path.isfile(subpath):
                hash, ext = os.path.splitext(entry)
                self.existingFiles[hash] = subpath 
        self.used = {}
        self.subBuffers = {}

    def cleanUp(self):
        for key in self.subBuffers:
            self.subBuffers[key].cleanUp()
        for hash in self.existingFiles:
            if not hash in self.used:
                os.remove(self.existingFiles[hash])

    def subBuffer(self, folderName):
        if not folderName in self.subBuffers:
            self.subBuffers[folderName] = FileBuffer(os.path.join(self.path, folderName))        
        return self.subBuffers[folderName]

    
    def useFileWithHash(self, hash):
        if hash in self.existingFiles:
            self.used[hash] = None
            return self.existingFiles[hash]
        else:
            return None

    def registerAndUseFileWithHash(self, hash, extension):
        self.existingFiles[hash] = os.path.join(self.path, hash+extension)
        self.used[hash] = None
        return self.existingFiles[hash]

    @staticmethod
    def hashFromData(data):
        return hashlib.sha256(data).hexdigest()
        
#     def pathForData(self, data):
#         return self.pathForHash(FileBuffer.hashFromData(data))
    

        