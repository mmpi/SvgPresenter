from RasterImageDrawer import RasterImageDrawer
from SvgDrawer import SvgDrawer
from PdfDrawer import PdfDrawer

DrawerGenerators = {"raster": lambda slide, log: RasterImageDrawer(slide.provideRasterImage(log)),
                    "svg":  lambda slide, log: SvgDrawer(slide.provideSvgFile(log)),
                    "pdf":  lambda slide, log: PdfDrawer(slide.providePdfFile(log)),}
