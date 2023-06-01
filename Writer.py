import openpyxl
import win32com.client
import datetime

from Constants import SPANISH_TO_ENGLISH_MONTHS_FULL, TIME_INTERVALS


def clean_fecha_consulta(date):
    try:
        # Split the date string into its components
        day_of_week, day, month, year = date.split()

        # Extract the day, month, and year from the parts list
        month = SPANISH_TO_ENGLISH_MONTHS_FULL.get(month, '')

        # Create a formatted date string
        formatted_date = f"{day}/{month}/{year[-2:]}"

        # Convert to datetime
        date = datetime.datetime.strptime(formatted_date, '%d/%b/%y')
    except ValueError:
        # Handle invalid date values by assigning None
        date = None

    return date


def create_prefix(output_folder, data):
    first_name = data['Nombre (s)']
    paterno = data['Apellido Paterno']
    materno = data['Apellido Materno']
    rfc = data['RFC']
    prefix = f'{output_folder}/{first_name}_{paterno}_{materno}_{rfc}'
    output_xlsx = f'{prefix}.xlsx'
    output_pdf = f'{prefix}.pdf'

    return output_xlsx, output_pdf


def generate_pdf_from_excel(xlsx_name, pdf_name):
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = False
    excel.DisplayAlerts = False  # disable alerts
    wb = None
    try:
        wb = excel.Workbooks.Open(xlsx_name)
        ws = wb.Worksheets['Resumen']
        ws.ExportAsFixedFormat(0, pdf_name)
    except Exception as e:
        print(e)
    finally:
        if wb is not None:
            wb.Close(False)  # Close the workbook, don't save changes
        excel.Quit()


def copy_template(xlsx_name):
    template_wb = openpyxl.load_workbook('Círculo Extractor Template.xlsx')
    template_wb.save(xlsx_name)


def process_extracted_data(output_folder, extracted_data_list):
    for extracted_data in extracted_data_list:
        general_information = extracted_data.general_information
        transactions = extracted_data.transactions
        inquiries = extracted_data.inquiries

        fecha_buro = clean_fecha_consulta(general_information['Fecha de consulta'])
        # Create the prefix name that will be used for the output pdf and xlsx files
        xlsx_name, pdf_name = create_prefix(output_folder=output_folder, data=general_information)

        # Create the xlsx file
        copy_template(xlsx_name)

        # Load the template workbook
        template_wb = openpyxl.load_workbook('Círculo Extractor Template.xlsx')

        # Get the 'Detalle de Cuentas' sheet
        sheet_name = 'Detalle de Cuentas'
        sheet = template_wb[sheet_name]

        # Write data to specific cells
        sheet['C4'] = fecha_buro
        sheet['C5'] = general_information['Folio consulta']
        sheet['C6'] = general_information['Folio consulta otra SIC']
        sheet['C7'] = general_information['Nombre (s)']
        sheet['C8'] = general_information['Apellido Paterno']
        sheet['C9'] = general_information['Apellido Materno']
        sheet['C10'] = general_information['Fecha de Nacimiento']
        sheet['C11'] = general_information['RFC']
        sheet['C12'] = general_information['CURP']

        sheet['E4'] = general_information['FICO Score']

        # Write general_information['Razones de Score'] to cells E5 and onwards
        row = 5
        for item in general_information['Razones de Score']:
            sheet[f'E{row}'] = item
            row += 1

        # Write transactions data to consecutive rows starting from row 17
        start_row = 17
        for i, (index, transaction) in enumerate(transactions.iterrows(), start=start_row):
            row = str(i)
            sheet[f'C{row}'] = transaction['Frequency']
            sheet[f'D{row}'] = transaction['Responsabilidad']
            sheet[f'E{row}'] = transaction['Credito']
            sheet[f'F{row}'] = transaction['Otorgante']
            sheet[f'G{row}'] = transaction['Plazo']
            sheet[f'H{row}'] = transaction['EstatusCAN']
            sheet[f'I{row}'] = transaction['Historial']
            sheet[f'J{row}'] = TIME_INTERVALS[transaction['Frequency']]
            sheet[f'K{row}'] = transaction['Limite']
            sheet[f'L{row}'] = transaction['Aprobado']
            sheet[f'M{row}'] = transaction['Actual']
            sheet[f'N{row}'] = transaction['Vencido']
            sheet[f'O{row}'] = transaction['A pagar']
            sheet[f'Q{row}'] = transaction['Reporte']
            sheet[f'R{row}'] = transaction['Apertura']
            sheet[f'S{row}'] = transaction['Cierre']
            sheet[f'T{row}'] = transaction['Pago']
            sheet[f'U{row}'] = transaction['Atraso']
            sheet[f'V{row}'] = transaction['Monto']
            sheet[f'W{row}'] = transaction['Fecha']
            sheet[f'X{row}'] = transaction['Situacion']

        # Get the 'Inquiries' sheet
        inquiries_sheet = template_wb['Consultas Realizadas']

        # Write inquiries data to consecutive rows starting from row 9
        start_row = 9
        for i, (index, inquiry) in enumerate(inquiries.iterrows(), start=start_row):
            row = str(i)
            inquiries_sheet[f'C{row}'] = inquiry['Fecha de Consulta']
            inquiries_sheet[f'D{row}'] = inquiry['Otorgante']
            inquiries_sheet[f'E{row}'] = inquiry['Tipo de Crédito']
            inquiries_sheet[f'F{row}'] = inquiry['Monto']
            inquiries_sheet[f'G{row}'] = inquiry['Moneda']

        # Save the modified workbook with the desired output file name
        template_wb.save(xlsx_name)
        template_wb.close()

