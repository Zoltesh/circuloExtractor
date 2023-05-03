import pdfrw
import pdfplumber
import os
from pathlib import Path


class Input_PDF:
    def __init__(self, filepath):
        self.filepath = filepath
        self.pdf = pdfrw.PdfReader(filepath)

    def get_text_content(self):
        """Extract the text content from each page of each PDF"""
        content = []
        for page in self.pdf.pages:
            text = page.Contents
            content.append(text)
        print(content)
        """ return content"""
