import subprocess

from fileConverter.BufferedFileConverter import BufferedFileConverter

class BufferedSvgToPdf(BufferedFileConverter):
    FileNameExtension = ".pdf"
    def convert(self, fromPath, toPath, log=None):
        if not log is None:
            log.write("Converting svg file to pdf...")
        # use inkscape to convert slide to pdf
        subprocess.check_output(["inkscape",
                                 "--without-gui",
                                 "--file="+fromPath,
                                 "--export-text-to-path",
                                 "--export-pdf="+toPath,])
        return True
    