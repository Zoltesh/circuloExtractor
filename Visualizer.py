from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer, KeepInFrame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.pagesizes import letter

import Processor
import Reader

flowables = []


# Create a title for the document
def output_title():
    # Define a style for your title
    title_style = ParagraphStyle(
        name='Title',
        fontSize=20,
        alignment=1,  # 1 for CENTER alignment
    )

    # Create your title with the style
    title = Paragraph("<u>Datos Clave del Análisis de la Sociedad Crediticia</u>", title_style)

    flowables.append(title)
    # Add a spacer after the title to create some vertical space
    flowables.append(Spacer(1, 50))  # Adjust the height as needed


def output_name(name):
    pass


def data_table_1(processed):
    # Create a list to store the table data
    table_data = [
        ["Header", "Total", "Not Old"],
        ["# créditos totales:", str(processed['Creditos Totales']), str(processed['Creditos Totales - Not Old'])],
        ["# créditos activos:", str(processed['Creditos Activos']), str(processed['Creditos Activos - Not Old'])],
        [f"# créditos atrasados:", str(processed['Creditos Atrasados']), str(processed['Creditos Atrasados - Not Old'])],
        [f"- filas {str(processed['Filas Atrasadas'])}"],
        ["Saldo actual", f"${str(processed['Saldo Actual'])}", f"${str(processed['Saldo Actual - Not Old'])}"],
        ["Pago mensual actual", f"${str(processed['Pago Mensual Actual'])}", f"${str(processed['Pago Mensual Actual - Not Old'])}"],
    ]

    # Create the table and set its style
    table = Table(table_data, colWidths=[110, 70, 70], rowHeights=30)
    table.setStyle(TableStyle([
        # Tuple values are (col, row)
        ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
        ('LINEBELOW', (0, 1), (-1, 1), 1, colors.black),
        ('LINEBELOW', (0, 2), (-1, 2), 1, colors.black),
        ('LINEBELOW', (1, 3), (-1, 3), 1, colors.black),
        ('LINEBELOW', (0, 4), (-1, 4), 1, colors.black),
        ('LINEABOVE', (0, -1), (-1, -1), 1, colors.black),
        ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
        ('LINEBEFORE', (0, 0), (0, -1), 1, colors.black),
        ('LINEAFTER', (0, 0), (0, -1), 1, colors.black),
        ('LINEAFTER', (-1, 0), (-1, -1), 1, colors.black),
        ('LINEBEFORE', (-1, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
    ]))

    # Create a KeepInFrame object and add your table to it
    keep_in_frame_1 = KeepInFrame(400, 200, [table], hAlign='LEFT')
    flowables.append(keep_in_frame_1)


def data_table_2(processed):
    # Create a list to store the table data
    table_data = [
        ["Header", "Value", "Fila"],
        ["Periodo más antiguo:", str(processed['Periodo Mas Antiguo'])],
        ["Saldo más grande (est):", str(processed['Saldo mas grande']), str(processed['Saldo mas grande - Row'])],
        ["Pago mens mayor (est):", f"${str(processed['Pagos mens mayor'])}", str(processed['Pagos mens mayor - Row'])],
        ["# consultas (ult. 12 meses):", str(processed['Consultas Ult 12 Meses'])],
        ["# consultas (ult. 24 meses):", str(processed['Consultas Ult 24 Meses'])]
    ]

    # Create the table and set its style
    table = Table(table_data, colWidths=[110, 80, 30], rowHeights=30)
    table.setStyle(TableStyle([
        # Tuple values are (col, row)
        ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),
        ('LINEABOVE', (0, 1), (-1, 1), 1, colors.black),
        ('LINEABOVE', (0, 2), (-1, 2), 1, colors.black),
        ('LINEABOVE', (0, 3), (-1, 3), 1, colors.black),
        ('LINEABOVE', (0, 4), (-1, 4), 1, colors.black),
        ('LINEABOVE', (0, 5), (-1, 5), 1, colors.black),
        ('LINEBELOW', (0, 5), (-1, 5), 1, colors.black),
        ('LINEBEFORE', (0, 0), (0, -1), 1, colors.black),
        ('LINEBEFORE', (1, 0), (1, -1), 1, colors.black),
        ('LINEBEFORE', (2, 0), (2, -1), 1, colors.black),
        ('LINEAFTER', (2, 0), (2, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black)
    ]))

    # Create a KeepInFrame object and add your table to it
    keep_in_frame_2 = KeepInFrame(400, 200, [table], hAlign='LEFT')
    flowables.append(keep_in_frame_2)


def bar_chart_1(processed):
    # Create a Drawing object to hold the chart
    drawing = Drawing(400, 200)

    # Create a VerticalBarChart object
    chart = VerticalBarChart()

    # Set the width of each bar
    chart.barWidth = 0.4

    # Set the space between each bar
    chart.groupSpacing = 0.2

    chart.barLabels.fontName = "Helvetica"
    chart.barLabels.fontSize = 12
    chart.barLabelFormat = '%d'
    chart.barLabels.nudge = -10

    # Set the data for the chart
    # Each sublist in chart.data represents a stack in a bar
    chart.data = [[float(processed['Saldo Actual - Not Old'])], [float(processed['Late Balance'])]]

    # Set the color for each bar in the chart
    chart.bars[0].fillColor = HexColor("#ED7D31")
    chart.bars[1].fillColor = HexColor("#4472C4")

    chart.categoryAxis.style = 'stacked'
    # Set the labels for the x-axis
    chart.categoryAxis.categoryNames = ['Your Label']

    # Add the chart to the drawing
    drawing.add(chart)

    # Add the drawing to your flowables
    flowables.append(drawing)


# Extract the data from Reader.py and process it in Processor.py
extracted_data = Reader.extract_data()
general = extracted_data.general_information
clean_records = Processor.clean_data(extracted_data.transactions)
cleaned_inquiries = Processor.clean_inquiries(extracted_data.inquiries)
processed_data = Processor.calculate_data(general, clean_records, cleaned_inquiries)

output_title()
data_table_1(processed=processed_data)
data_table_2(processed=processed_data)


# Create a Spacer to add space between the tables
spacer = Spacer(0, 20)
flowables.append(spacer)

bar_chart_1(processed=processed_data)


# Create a PDF document
doc = SimpleDocTemplate("testy.pdf", pagesize=letter, leftMargin=18, rightMargin=18)

# Build the document with the flowables
doc.build(flowables)
