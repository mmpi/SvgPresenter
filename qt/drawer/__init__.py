from RasterImageDrawer import RasterImageDrawer
from PdfDrawer import PdfDrawer
from SvgDrawer import SvgDrawer
from SvgRasterDrawer import SvgRasterDrawer

DrawerGenerators = {"raster": lambda slide, log: RasterImageDrawer(slide.provideRasterImage(log)),
                    "pdf":  lambda slide, log: PdfDrawer(slide.providePdfFile(log)),
                    "svg":  lambda slide, log: SvgDrawer(slide.provideSvgFile(log)),
                    "svgRaster":  lambda slide, log: SvgRasterDrawer(slide, log),}
