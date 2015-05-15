import subprocess

from fileConverter.BufferedFileConverter import BufferedFileConverter

class BufferedPdfToSvg(BufferedFileConverter):
    FileNameExtension = ".svg"
    def convert(self, fromPath, toPath, log=None):
        if not log is None:
            log.write("Converting pdf file to svg...")
#         # use pdftosvg to convert slide to svg (without flowed text)
#         subprocess.check_output(["pdf2svg", fromPath, toPath,])
        # use inkscape to convert slide to svg again
        subprocess.check_output(["inkscape",
                                 "--without-gui",
                                 "--file="+fromPath,
                                 "--export-plain-svg="+toPath,])
        return True
