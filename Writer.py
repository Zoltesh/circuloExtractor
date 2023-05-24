import Reader
import Processor
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate
"""from Visualizer import create_table_page_1"""


def generate_pdf(filename, data):
    # Create a new PDF document
    doc = SimpleDocTemplate(filename, pagesize=letter)

    # Create the flowables for the document
    flowables = create_table_page_1(data)

    # Build the document with the flowables
    doc.build(flowables)


# Generate the PDF using the extracted and processed data
# Note: Please ensure that 'Output Filename' is correctly set in the processed data.
generate_pdf(processed_data['Output Filename'], processed_data)
