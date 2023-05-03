from reportlab.pdfgen import canvas
import pdfrw


class Output_PDF:
    def __init__(self, template_filepath, output_filepath):
        self.output_filepath = output_filepath
        self.template = pdfrw.PdfReader(template_filepath)
        self.pages = self.template.pages
        self.canvas = canvas.Canvas(output_filepath)
        self.page_number = 1

    def add_text(self, text, x, y):
        """Add text to the current page of the PDF at the specified coordinates"""
        if text is None:
            text = "test"  # Set a default value if text is None
            Canvas = pdfrw.PageMerge().add(self.pages[self.page_number - 1])[0]
            Canvas.drawString(x, y, text)

    def next_page(self):
        """Advance to the next page of the PDF"""
        self.page_number += 1

    def save(self):
        """Save the PDF file"""
        self.canvas.save()
