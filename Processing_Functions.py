import re
import os
from datetime import datetime
import pandas as pd
import fitz
import pdfplumber
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from dateutil.parser import parse

from Payment_History_Processor import extract_payment_history, process_payment_history


def convert_spanish_date(date_str):
    months = {
        "Enero": "January",
        "Febrero": "February",
        "Marzo": "March",
        "Abril": "April",
        "Mayo": "May",
        "Junio": "June",
        "Julio": "July",
        "Agosto": "August",
        "Septiembre": "September",
        "Octubre": "October",
        "Noviembre": "November",
        "Diciembre": "December"
    }

    for spanish_month, english_month in months.items():
        date_str = date_str.replace(spanish_month, english_month)

    return parse(date_str).strftime("%d-%b-%Y")


def extract_payment_history_data(table):
    # Call the process_payment_history function from Payment_History_Processor.py
    payment_history_df = process_payment_history(table)
    return payment_history_df


def extract_data_with_pattern(text, pattern, process_data):
    match = pattern.search(text)
    if match:
        return process_data(match)
    else:
        return None


def process_fico_score(match):
    fico_score = match.group(1)
    data = [{"Heading": "FICO Score", "Value": fico_score}]
    return pd.DataFrame(data)


def process_razones_de_score(match):
    line = match.group(1).split("\n")[0]
    codes = line.replace(" ", "").split(',')
    data = [{"Heading": f"Razón de Score {i + 1}", "Value": code} for i, code in enumerate(codes)]
    return pd.DataFrame(data)


def process_folio_con(match):
    folio = match.group(1)
    data = [{"Heading": "Folio Con", "Value": folio}]
    return pd.DataFrame(data)


def process_fol_con_o_sic(match):
    folio = match.group(1)
    data = [{"Heading": "Fol Con o SIC", "Value": folio}]
    return pd.DataFrame(data)


def process_nombre(match):
    nombre = match.group(1).strip()
    data = [{"Heading": "Nombre", "Value": nombre}]
    return pd.DataFrame(data)


def process_ap_paterno(match):
    ap_paterno = match.group(1)
    data = [{"Heading": "Ap Patern", "Value": ap_paterno}]
    return pd.DataFrame(data)


def process_ap_materno(match):
    ap_materno = match.group(1)
    data = [{"Heading": "Ap Matern", "Value": ap_materno}]
    return pd.DataFrame(data)


def process_fecha_nacimiento(match):
    fecha_nacimiento = datetime.strptime(match.group(1), "%d/%b/%y").strftime("%d-%b-%y")
    data = [{"Heading": "Fecha de Nac", "Value": fecha_nacimiento}]
    return pd.DataFrame(data)


def process_fecha_buro(match):
    date = convert_spanish_date(match.group(1))
    data = [{"Heading": "Fecha Buró", "Value": date}]
    return pd.DataFrame(data)


def process_rfc(match):
    rfc = match.group(1)
    data = [{"Heading": "RFC", "Value": rfc}]
    return pd.DataFrame(data)


def process_curp(match):
    curp = match.group(1)
    data = [{"Heading": "CURP", "Value": curp}]
    return pd.DataFrame(data)


# Extract data from a single pdf and create a pandas dataframe
def extract_and_process_pdf(input_path: str):
    # Extract text from the input PDF
    text = ''
    with fitz.open(input_path) as pdf:
        for page in pdf:
            text += page.get_text()

        # Extract the RFC
        rfc_match = re.search(r"RFC:\s*([A-Za-z0-9]+)", text)
        if rfc_match:
            rfc = rfc_match.group(1)
        else:
            rfc = "unknown"

        # Process the extracted text and create a pandas DataFrame (data structure)
        dfs = []

        fico_score_pattern = re.compile(r'FICO\W+Score\s+(\d+)')
        fico_score_df = extract_data_with_pattern(text, fico_score_pattern, process_fico_score)
        if fico_score_df is not None:
            dfs.append(fico_score_df)

        razones_de_score_pattern = re.compile(r'Razones de Score:\s*([\w\s,]+)')
        razones_de_score_df = extract_data_with_pattern(text, razones_de_score_pattern, process_razones_de_score)
        if razones_de_score_df is not None:
            dfs.append(razones_de_score_df)

        fecha_buro_pattern = re.compile(r"Fecha de consulta:\s*(?:\w{1,10}\s+)?(\d{1,2}\s+\w+\s+\d{4})")
        fecha_buro_df = extract_data_with_pattern(text, fecha_buro_pattern, process_fecha_buro)
        if fecha_buro_df is not None:
            dfs.append(fecha_buro_df)

        folio_con_pattern = re.compile(r"Folio consulta:\s*([\w]+)")
        folio_con_df = extract_data_with_pattern(text, folio_con_pattern, process_folio_con)
        if folio_con_df is not None:
            dfs.append(folio_con_df)

        fol_con_o_sic_pattern = re.compile(r"Folio consulta otra SIC:\s*([\w]+)")
        fol_con_o_sic_df = extract_data_with_pattern(text, fol_con_o_sic_pattern, process_fol_con_o_sic)
        if fol_con_o_sic_df is not None:
            dfs.append(fol_con_o_sic_df)

        # Update the nombre_pattern
        nombre_pattern = re.compile(r"Nombre\s\(s\):\s+([\w\s]+)\s*Apellido Paterno")
        nombre_df = extract_data_with_pattern(text, nombre_pattern, process_nombre)
        if nombre_df is not None:
            dfs.append(nombre_df)

        ap_paterno_pattern = re.compile(r"Apellido Paterno:\s*([\w\s]+?)\s*\n")
        ap_paterno_df = extract_data_with_pattern(text, ap_paterno_pattern, process_ap_paterno)
        if ap_paterno_df is not None:
            dfs.append(ap_paterno_df)

        ap_materno_pattern = re.compile(r"Apellido Materno:\s*([\w\s]+?)\s*\n")
        ap_materno_df = extract_data_with_pattern(text, ap_materno_pattern, process_ap_materno)
        if ap_materno_df is not None:
            dfs.append(ap_materno_df)

        fecha_nacimiento_pattern = re.compile(r"Fecha de Nacimiento:\s*(\d{1,2}/\w+/\d{2})")
        fecha_nacimiento_df = extract_data_with_pattern(text, fecha_nacimiento_pattern, process_fecha_nacimiento)
        if fecha_nacimiento_df is not None:
            dfs.append(fecha_nacimiento_df)

        rfc_pattern = re.compile(r"RFC:\s*([A-Za-z0-9]+)")
        rfc_df = extract_data_with_pattern(text, rfc_pattern, process_rfc)
        if rfc_df is not None:
            dfs.append(rfc_df)

        curp_pattern = re.compile(r"CURP:\s*([A-Za-z0-9]+)")
        curp_df = extract_data_with_pattern(text, curp_pattern, process_curp)
        if curp_df is not None:
            dfs.append(curp_df)

        # Extract payment history data
        payment_history_df = extract_payment_history(pdf)

        # Add payment_history_df to dfs if not empty
        if payment_history_df is not None and not payment_history_df.empty:
            dfs.append(payment_history_df)

        if dfs:
            result_df = pd.concat(dfs, axis=0, ignore_index=True)
            return rfc, result_df, payment_history_df
        else:
            print("No data found in the PDF")
            return rfc, None, payment_history_df


# Create prepare data from a single dataframe to create data visualizations and fill out the output pdf
def process_dataframe(input_path: str, output_path: str):
    # Process each PDF in the input folder
    for file in os.listdir(input_path):
        if file.endswith(".pdf"):
            file_path = os.path.join(input_path, file)

            # Extract text from the input PDF
            text = ''
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text()
            print(text)

            # Process the extracted text, create data structures, etc.

            # Save the output PDF to the output folder
            output_file_path = os.path.join(output_path, file)


def create_output_pdf(data: pd.DataFrame, output_path: str):
    # Prepare the output PDF using reportlab
    doc = SimpleDocTemplate(output_path, pagesize=letter)

    # Create a table with the extracted data
    table_data = [["Heading", "Value"]] + data.values.tolist()
    table = Table(table_data)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 14),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )

    # Add the table to the PDF and build it
    doc.build([table])
