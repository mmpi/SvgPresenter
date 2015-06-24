import subprocess

from fileConverter.BufferedFileConverter import BufferedFileConverter

class BufferedSvgToPlainSvg(BufferedFileConverter):
    FileNameExtension = ".svg"
    def convert(self, fromPath, toPath, log=None):
        if not log is None:
            log.write("Converting svg file to plain svg...")
        # use inkscape to convert slide to pdf
        subprocess.check_output(["inkscape",
                                 "--without-gui",
                                 "--file="+fromPath,
                                 "--export-area-page",
                                 "--export-text-to-path",
                                 "--export-plain-svg="+toPath,])
        if not log is None:
            log.write("Done: %s"%toPath)
        return True
        