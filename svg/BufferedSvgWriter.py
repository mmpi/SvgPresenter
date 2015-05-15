from buffer.BufferedFileFilter import BufferedFileFilter


class BufferedSvgWriter(BufferedFileFilter):
    FileNameExtension = ".svg"
    def createFileFromData(self, path, data):
        file = open(path, 'wb')
        file.write(data)
        file.close()
        return True

    write = BufferedFileFilter.filterData
    