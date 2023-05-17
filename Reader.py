import camelot
import fitz
import pandas as pd
import matplotlib
from Logger import configure_logging
from Constants import POSITIONS
logger = configure_logging()

# Constants
PDF_PATH = 'Z:/Code/Credit Report Summary/New Example Input/Example input.pdf'
CURP_STR = "CURP:"


class ExtractedData:
    def __init__(self):
        self.general_information = {}
        self.credit_score = {}
        self.credit_pie_charts = {}
        self.transactions = []


matplotlib.use('TkAgg')  # or 'Qt5Agg'

# Set pandas display options
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)


def is_valid_table(table):
    # Check if the table has at least 3 rows and 20 columns
    return table.df.shape[0] >= 3 and table.df.shape[1] >= 20


def extract_general_information(text):
    general_information = {}

    # Getting Folio consulta otra SIC and Folio consulta since they appear immediately on the first 2 lines
    folio_consulta, folio_consulta_otra_sic = text.splitlines()[:2]
    general_information['Folio consulta'] = folio_consulta.strip()
    general_information['Folio consulta otra SIC'] = folio_consulta_otra_sic.strip()

    # Other General info starts after the string "CURP: "
    curp_idx = text.find("CURP:")
    if curp_idx != -1:
        curp_text = text[curp_idx + len("CURP:"):].strip()
        names = curp_text.splitlines()[:10]
        general_information['Nombre (s)'] = names[0] if len(names) > 0 else None
        general_information['Apellido Paterno'] = names[1] if len(names) > 1 else None
        general_information['Apellido Materno'] = names[2] if len(names) > 2 else None
        general_information['Fecha de Nacimiento'] = names[3] if len(names) > 3 else None
        general_information['RFC'] = names[4] if len(names) > 4 else None
        general_information['CURP'] = names[5] if len(names) > 5 else None
        general_information['FICO Score'] = names[6] if len(names) > 6 else None
        general_information['Razones de Score'] = \
            [rs.strip() for rs in names[7].replace("Razones de Score: ", "").split(',')]
        """general_information['Fecha de consulta'] = names[22] if len(names > 22) else None"""
    else:
        general_information['Nombre (s)'] = None
        general_information['Apellido Paterno'] = None
        general_information['Apellido Materno'] = None
        general_information['Fecha de Nacimiento'] = None
        general_information['RFC'] = None
        general_information['CURP'] = None
        general_information['FICO Score'] = None
        general_information['Razones de Score'] = None
    general_information['Fecha de consulta'] = text[113:].split('\n', 1)[0]
    return general_information


def extract_credit_data(table, positions):
    records = []
    # Iterate over the rows of the DataFrame in steps of 3 (assuming each record is 3 rows long)
    for start_row in range(2, len(table.df), 3):  # Start from row 3
        if start_row + 2 >= len(table.df):  # Check if the record has all three rows
            break  # If not, break out of the loop
        record = {}
        for key, (row_offset, col) in positions.items():
            record[key] = table.df.iloc[start_row + row_offset, col]
        records.append(record)

    return records


def extract_data():
    try:
        with fitz.open(PDF_PATH) as pdf:
            extracted_data = ExtractedData()

            page_1 = pdf.load_page(0)
            text = page_1.get_text()

            extracted_data.general_information = extract_general_information(text)

            logger.debug("General information extracted")

            # Extract tables from all pages
            tables = camelot.read_pdf(PDF_PATH, pages='all', flavor='lattice', line_scale=100)

            # Iterate over all tables
            for table in tables:
                # Check if the table is valid
                if not is_valid_table(table):
                    continue  # Skip this table

                # Extract credit data from the table
                records = extract_credit_data(table, POSITIONS)
                extracted_data.transactions.extend(records)

            logger.debug("Credit data extracted")

    except fitz.fitz.FileDataError:
        logger.error(f"Cannot open broken document: {PDF_PATH}")

    return extracted_data

