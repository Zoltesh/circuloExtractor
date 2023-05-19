from reportlab.lib.enums import TA_LEFT, TA_CENTER

import Reader
import Processor
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def generate_pdf(filename, processed_data):
    # Create a new PDF document
    doc = SimpleDocTemplate(filename, pagesize=letter)
    # Define styles for the document
    styles = getSampleStyleSheet()

    # Create a list to store the flowables (content) of the document
    flowables = []

    # Create a custom paragraph style for the title
    title_style = ParagraphStyle(
        name='TitleStyle',
        parent=styles['Title'],
        alignment=TA_LEFT,
        fontName='Helvetica-Bold',
        underline=True,
    )

    # Add a title to the document
    title = Paragraph("<u>Datos Clave del Análisis de la Sociedad Crediticia</u>", title_style)
    flowables.append(title)
    flowables.append(Spacer(1, 20))

    # page 1 style
    page_1_style = ParagraphStyle(
        name='DataStyle',
        parent=styles['Normal'],
        alignment=TA_LEFT,
    )

    # Create a table to align the columns
    table_data = [
        [
            Paragraph("<u>Header</u>",
                      ParagraphStyle(name='HeaderStyle', alignment=TA_CENTER, fontName='Helvetica-Bold')),
            Paragraph("<u>Total</u>",
                      ParagraphStyle(name='HeaderStyle', alignment=TA_CENTER, fontName='Helvetica-Bold')),
            Paragraph("<u>Not Old</u>",
                      ParagraphStyle(name='HeaderStyle', alignment=TA_CENTER, fontName='Helvetica-Bold')),
        ],
        [
            Paragraph("# créditos totales:", ParagraphStyle(name='DataStyle', alignment=TA_LEFT)),
            Paragraph(str(processed_data['Creditos Totales']), ParagraphStyle(name='DataStyle', alignment=TA_CENTER)),
            Paragraph(str(processed_data['Creditos Totales - Not Old']),
                      ParagraphStyle(name='DataStyle', alignment=TA_CENTER)),
        ],
        [
            Paragraph("# créditos activos:", ParagraphStyle(name='DataStyle', alignment=TA_LEFT)),
            Paragraph(str(processed_data['Creditos Activos']), ParagraphStyle(name='DataStyle', alignment=TA_CENTER)),
            Paragraph(str(processed_data['Creditos Activos - Not Old']),
                      ParagraphStyle(name='DataStyle', alignment=TA_CENTER)),
        ],
        [
            Paragraph(f"# créditos atrasados:", ParagraphStyle(name='DataStyle', alignment=TA_LEFT)),
            Paragraph(str(processed_data['Creditos Atrasados']), ParagraphStyle(name='DataStyle', alignment=TA_CENTER)),
            Paragraph(str(processed_data['Creditos Atrasados - Not Old']),
                      ParagraphStyle(name='DataStyle', alignment=TA_CENTER)),
        ],
        [
            Paragraph(f" - filas {str(processed_data['Filas Atrasadas'])}", ParagraphStyle(name='DataStyle', alignment=TA_CENTER)),
        ],
        [
            Paragraph("Saldo actual", ParagraphStyle(name='DataStyle', alignment=TA_LEFT)),
            Paragraph(f"${str(processed_data['Saldo Actual'])}", ParagraphStyle(name='DataStyle', alignment=TA_CENTER)),
            Paragraph(f"${str(processed_data['Saldo Actual - Not Old'])}", ParagraphStyle(name='DataStyle',
                                                                                          alignment=TA_CENTER)),
        ],
        [
            Paragraph("Pago mensual actual", ParagraphStyle(name='DataStyle', alignment=TA_LEFT)),
            Paragraph(f"${str(processed_data['Pago Mensual Actual'])}", ParagraphStyle(name='DataStyle', alignment=TA_CENTER)),
            Paragraph(f"${str(processed_data['Pago Mensual Actual - Not Old'])}",
                      ParagraphStyle(name='DataStyle', alignment=TA_CENTER)),
        ],
    ]

    # Create the table and set its style
    table = Table(table_data, colWidths=[150, 75, 75], rowHeights=30)
    table.setStyle(TableStyle([
        # Tuple values are (col, row)
        ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),

        ('LINEBELOW', (0, 1), (-1, 1), 1, colors.black),
        ('LINEBELOW', (0, 2), (-1, 2), 1, colors.black),
        ('LINEBELOW', (0, 4), (-1, 4), 1, colors.black),

        ('LINEABOVE', (0, -1), (-1, -1), 1, colors.black),  # Add a line above the last row
        ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),  # Add a line above the last row

        ('LINEBEFORE', (0, 0), (0, -1), 1, colors.black),
        ('LINEAFTER', (0, 0), (0, -1), 1, colors.black),

        ('LINEAFTER', (-1, 0), (-1, -1), 1, colors.black),
        ('LINEBEFORE', (-1, 0), (-1, -1), 1, colors.black),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
    ]))

    flowables.append(table)
    flowables.append(Spacer(1, 20))

    # Add the remaining data to the document
    data = [
        Paragraph(f"Periodo más antiguo: 21-mar-13", page_1_style),
        Paragraph(
            f"Saldo más grande (est): ${processed_data['Saldo mas grande']} (fila {processed_data['Saldo mas grande - Row']})",
            page_1_style
        ),
        Paragraph(
            f"Pago mens mayor (est): ${processed_data['Pagos mens mayor']} (fila {processed_data['Pagos mens mayor - Row']})",
            page_1_style
        ),
        Paragraph(f"# consultas (ult. 12 meses): {processed_data['Consultas Ult 12 Meses']}", page_1_style),
        Paragraph(f"# consultas (ult. 24 meses): {processed_data['Consultas Ult 24 Meses']}", page_1_style),
    ]

    flowables.extend(data)

    # Build the document with the flowables
    doc.build(flowables)


# Extract the data from Reader.py and process it in Processor.py

# Extract the data
extracted_data = Reader.extract_data()

# Assign general data
general = extracted_data.general_information

# Clean the data
clean_records = Processor.clean_data(extracted_data.transactions)

# Clean inquiries
cleaned_inquiries = Processor.clean_inquiries(extracted_data.inquiries)

processed_data = Processor.calculate_data(general, clean_records, cleaned_inquiries)

# Generate the PDF using the extracted and processed data
generate_pdf(processed_data['Output Filename'], processed_data)
