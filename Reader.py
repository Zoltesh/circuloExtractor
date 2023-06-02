import camelot
import fitz
import re
import pandas as pd
import matplotlib
from Logger import configure_logging

logger = configure_logging(__name__)


def open_pdf(path):
    try:
        with fitz.open(path) as pdf:
            page_1 = pdf.load_page(0)
            text = page_1.get_text()
            general_info = extract_general_information(text)
            logger.debug("General information extracted")

            tables = camelot.read_pdf(str(path), pages='all', flavor='lattice', line_scale=100)

            return general_info, tables

    except fitz.fitz.FileDataError:
        logger.error(f"Cannot open broken document: {path}")
        return None


CURP_STR = "CURP:"

matplotlib.use('TkAgg')  # or 'Qt5Agg'

# Set pandas display options
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)


def is_valid_credit(table):
    """
    Checks if a table contains valid credit records.

    Args:
        table (camelot.core.Table): The table to check.

    Returns:
        bool: True if the table contains valid credit records, False otherwise.

    Raises:
        ValueError: If the table object is invalid.

    """

    # Check if the table has at least 3 rows and 20 columns
    return table.df.shape[0] >= 3 and table.df.shape[1] >= 20


def is_valid_inquiry(table):
    """
    Checks if a table contains valid inquiry records.

    Args:
        table (camelot.core.Table): The table to check.

    Returns:
        bool: True if the table contains valid inquiry records, False otherwise.

    Raises:
        ValueError: If the table object is invalid.

    """

    if not isinstance(table, camelot.core.Table):
        raise ValueError("Invalid table object")

    cols = {'Fecha de Consulta', 'Otorgante', 'Tipo de Crédito', 'Monto', 'Moneda'}
    if table.df.shape[1] == 5:
        return all(col in cols for col in table.df.iloc[0, :])
    else:
        return False


# General information found on the first page and is not structured in a tabular format
# Here we use PyMuPDF (fitz) to extract the text based on its location on the page
def extract_general_information(text):
    """
    Extracts general information from the provided text.

    Args:
        text (str): The text to extract information from.

    Returns:
        dict: A dictionary containing the extracted general information.

    """

    general_information = {}

    # Extracting Folio consulta otra SIC and Folio consulta since they appear immediately on the first 2 lines
    lines = text.split('\n')
    folio_consulta = lines[0].strip()
    folio_consulta_otra_sic = lines[1].strip() if len(lines) > 1 else ''

    general_information['Folio consulta'] = folio_consulta
    general_information['Folio consulta otra SIC'] = folio_consulta_otra_sic

    # Other general info starts after the string "CURP: "
    curp_idx = text.find("CURP:")
    if curp_idx != -1:
        curp_text = text[curp_idx + len("CURP:"):].strip()
        names = curp_text.splitlines()[:10]

        # Assigning values to the corresponding keys in the general_information dictionary
        keys = ['Nombre (s)', 'Apellido Paterno', 'Apellido Materno', 'Fecha de Nacimiento', 'RFC',
                'CURP', 'FICO Score']
        for index, key in enumerate(keys):
            general_information[key] = names[index] if index < len(names) else None

        # Extracting Razones de Score if present
        razones_de_score = re.search(r"Razones de Score: (.*)", names[7])
        if razones_de_score:
            razones_de_score_values = razones_de_score.group(1).split(',')
            general_information['Razones de Score'] = [value.strip() for value in razones_de_score_values]
        else:
            general_information['Razones de Score'] = None
    else:
        # If CURP is not found, assign None to all general information keys
        keys = ['Nombre (s)', 'Apellido Paterno', 'Apellido Materno', 'Fecha de Nacimiento', 'RFC',
                'CURP', 'FICO Score', 'Razones de Score']
        for key in keys:
            general_information[key] = None

    # Extracting Fecha de consulta from a specific position in the text
    general_information['Fecha de consulta'] = text[113:].split('\n', 1)[0]

    return general_information


def extract_credit_data(table, positions):
    """
    Extracts credit data from a table.

    Args:
        table (camelot.core.Table): The table to extract data from.
        positions (dict): A dictionary mapping keys to (row_offset, col) positions in the table.

    Returns:
        list: A list of dictionaries representing the extracted credit records.

    """

    records = []
    rows_to_change = ['Limite', 'Aprobado', 'Actual', 'Vencido', 'A pagar']
    # Iterate over the rows of the DataFrame in steps of 3 (assuming each record is 3 rows long)
    for start_row in range(2, len(table.df), 3):  # Start from row 3
        if start_row + 2 >= len(table.df):  # Check if the record has all three rows
            break  # If not, break out of the loop
        record = {}
        for key, (row_offset, col) in positions.items():
            value = table.df.iloc[start_row + row_offset, col]
            if key in rows_to_change and value == '0':
                value = 0
            record[key] = value
        records.append(record)

    return records


def extract_consultas_realizadas(table, positions):
    """
    Extracts the "Consultas Realizadas" data from the provided table.

    Args:
        table (camelot.core.Table): The table containing the "Consultas Realizadas" data.
        positions (dict): A dictionary mapping keys to (row, col) positions in the table.

    Returns:
        list: A list of dictionaries representing the extracted "Consultas Realizadas" records.

    """

    inquiries = []
    # Iterate over the rows and extract the data
    for start_row in range(1, len(table.df)):  # Start from row 1
        inquiry = {}
        for key, (row, col) in positions.items():
            inquiry[key] = table.df.iloc[start_row, col]
        inquiries.append(inquiry)
    return inquiries
