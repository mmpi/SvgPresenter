import subprocess

from fileConverter.BufferedFileConverter import BufferedFileConverter

class BufferedSvgToPng(BufferedFileConverter):
    FileNameExtension = ".png"
    def convert(self, fromPath, toPath, log=None):
        if not log is None:
            log.write("Converting svg file to png...")
        # use inkscape to convert slide to png
        subprocess.check_output(["inkscape",
                                 "--without-gui",
                                 "--file="+fromPath,
                                 "--export-background-opacity=1.0",
                                 "--export-png="+toPath,])
        return True
