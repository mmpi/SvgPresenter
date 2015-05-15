import subprocess

from fileConverter.BufferedFileConverter import BufferedFileConverter

class BufferedSvgToPng(BufferedFileConverter):
    FileNameExtension = ".png"
    def convert(self, fromPath, toPath, log=None, width=None, height=None):
        if not log is None:
            log.write("Converting svg file to png...")
        sizeParameters = []
        if not width is None:
            sizeParameters.append("--export-width=%d"%width)  
        if not height is None:
            sizeParameters.append("--export-height=%d"%height)  
        
        # use inkscape to convert slide to png
        subprocess.check_output(["inkscape",
                                 "--without-gui",
                                 "--file="+fromPath,
                                 "--export-background-opacity=1.0",]
                                + sizeParameters
                                + ["--export-png="+toPath,])
        return True
