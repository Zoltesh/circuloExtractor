# Extract the raw data from a single input pdf

# This is the PyMuPDF library
import fitz
import re
from Logger import configure_logging

logger = configure_logging()


class ExtractedData:
    def __init__(self):
        self.general_information = {}
        self.credit_score = {}
        self.credit_pie_charts = {}
        self.transactions = []


def extract_pdf_data(file_path):
    logger.info(f"Processing file: {file_path}")
    try:
        # Read the PDF using PyMuPDF
        with fitz.open(file_path) as pdf:
            # Extract data from the PDF
            extracted_data = ExtractedData()

            # ------------------------------- Extract general information ----------------------------------------------
            page_1 = pdf.load_page(0)
            text = page_1.get_text()
            # Getting Folio consulta otra SIC and Folio consulta since they appear immediately on the first 2 lines
            folio_consulta, folio_consulta_otra_sic = text.splitlines()[:2]
            extracted_data.general_information['Folio consulta'] = folio_consulta.strip()
            extracted_data.general_information['Folio consulta otra SIC'] = folio_consulta_otra_sic.strip()
            # Other General info starts after the string "CURP: "
            curp_idx = text.find("CURP:")
            if curp_idx != -1:
                curp_text = text[curp_idx + len("CURP:"):].strip()
                names = curp_text.splitlines()[:10]
                extracted_data.general_information['Nombre (s)'] = names[0] if len(names) > 0 else None
                extracted_data.general_information['Apellido Paterno'] = names[1] if len(names) > 1 else None
                extracted_data.general_information['Apellido Materno'] = names[2] if len(names) > 2 else None
                extracted_data.general_information['Fecha de Nacimiento'] = names[3] if len(names) > 3 else None
                extracted_data.general_information['RFC'] = names[4] if len(names) > 4 else None
                extracted_data.general_information['CURP'] = names[5] if len(names) > 5 else None
                extracted_data.general_information['FICO Score'] = names[6] if len(names) > 6 else None
                extracted_data.general_information['Razones de Score'] = \
                    [rs.strip() for rs in names[7].replace("Razones de Score: ", "").split(',')]

            else:
                extracted_data.general_information['Nombre (s)'] = None
                extracted_data.general_information['Apellido Paterno'] = None
                extracted_data.general_information['Apellido Materno'] = None
                extracted_data.general_information['Fecha de Nacimiento'] = None
                extracted_data.general_information['RFC'] = None
                extracted_data.general_information['CURP'] = None
                extracted_data.general_information['FICO Score'] = None
                extracted_data.general_information['Razones de Score'] = None

            logger.debug("General information extracted")
            print("General information:", extracted_data.general_information)
            # -------------------------------------- END ---------------------------------------------------------------
            # -------------------------------- Extract transactions table ----------------------------------------------
            transactions = []
            column_names = ["Producto Responsabilidad", "Otorgante", "Limite", "Aprobado", "Actual", "A pagar",
                            "Reporte", "Cierre", "Pago", "Atraso", "Monto", "Situacion", "Plazo", "Apertura", "Fecha",
                            "Vencido", "Credito", "Historial de Pago", "Frequencia", "ID"]

            frequencia_values = ["Semanal", "Catorcenal", "Quincenal", "Mensual", "Bimestral", "Trimestral",
                                 "Cuatrimestral", "Semestral", "Anual"]

            # TODO Obtain Producto Responsabilidad for each record, adapting to differing line counts
            """Could find by getting first transaction on a page where the line above is Estatus\nCAN..."""
            # TODO Obtain Otorgante for each record, adapting to differing line counts
            # TODO Obtain Limite for each record and convert to number
            # TODO Obtain Aprobado for each record and convert to number
            # TODO Obtain Actual for each record and convert to number
            # TODO Obtain A pagar for each record and convert to number
            # TODO Obtain Reporte for each record and convert to a date
            # TODO Obtain Cierre for each record and convert to a date
            # TODO Obtain Pago for each record and convert to a date
            # TODO Obtain Atraso for each record and convert to a number
            # TODO Obtain Monto for each record and convert to a number
            # TODO Obtain Situacion for each record, adapting to differing line counts
            # TODO Obtain Plazo for each record and convert to a number
            # TODO Obtain Apertura for each record and convert to a date
            # TODO Obtain Fecha for each record and convert to a date
            # TODO Obtain Vencido for each record and convert to a number
            # TODO Obtain Credito for each record, adapting to differing line counts
            # TODO Obtain Historial de Pago for each record
            # TODO Obtain Frequencia for each record
            # TODO Obtain ID for each record, accounting for double digit numbers on separate lines
            # -------------------------------------- END ---------------------------------------------------------------
        logger.info(f"Finished reading file: {file_path}")
        return extracted_data
    except fitz.fitz.FileDataError:
        logger.error(f"Cannot open broken document: {file_path}")
        return None
