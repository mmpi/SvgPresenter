import popplerqt4

class PdfDrawer:
    def __init__(self, fileName):
        self.document = popplerqt4.Poppler.Document.load(fileName)
#         self.document.setRenderBackend(self.document.ArthurBackend)
        self.document.setRenderHint(self.document.Antialiasing)
        self.document.setRenderHint(self.document.TextAntialiasing)
        self.page = self.document.page(0)
        self.pageWidth = self.page.pageSizeF().width()*90.0/72.0
    def __call__(self, painter):
        size = painter.window()
        factor = size.width()*1.0/self.pageWidth
#         self.page.renderToPainter(painter, factor*90, factor*90, 0, 0, size.width(), size.height())
        img = self.page.renderToImage(factor*90, factor*90, 0, 0, size.width(), size.height())
        painter.drawImage(painter.window(), img)
        