import pandas as pd
from Reader import extract_credit_data, extract_consultas_realizadas, is_valid_inquiry, \
    is_valid_credit, open_pdf
from Logger import configure_logging
from Constants import POSITIONS, INQUIRY_POSITIONS

logger = configure_logging(__name__)


class ExtractedData:
    """
    A class to store the extracted data from the credit report.

    Attributes:
        general_information (dict): Dictionary to store general information.
        credit_score (dict): Dictionary to store credit score information.
        transactions (list): List to store transaction records.

    """

    def __init__(self):
        self.general_information = {}
        self.credit_score = {}
        self.transactions = []
        self.inquiries = []


# Uses PyMuPDF (fitz) to extract the general text info from page 1
# Uses Camelot to extract the tabular data for the records on pages 2+
def process_data(path):
    general_info, tables = open_pdf(path)

    extracted_data = ExtractedData()
    extracted_data.general_information = general_info

    for table in tables:
        if is_valid_credit(table):
            records = extract_credit_data(table, POSITIONS)
            extracted_data.transactions.extend(records)

        elif is_valid_inquiry(table):
            consultas_realizadas = extract_consultas_realizadas(table, INQUIRY_POSITIONS)
            extracted_data.inquiries.extend(consultas_realizadas)
            logger.info("Consultas Realizadas extracted successfully")

    logger.debug("Credit data and Consultas Realizadas extracted")

    extracted_data.transactions = pd.DataFrame(extracted_data.transactions)
    extracted_data.inquiries = pd.DataFrame(extracted_data.inquiries)

    return extracted_data

