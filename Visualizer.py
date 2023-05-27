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
        fontSize=16,
        alignment=0,
    )

    # Create your title with the style
    title = Paragraph("<u>Datos Clave del Análisis de la Sociedad Crediticia</u>", title_style)

    flowables.append(title)
    # Add a spacer after the title to create some vertical space
    flowables.append(Spacer(1, 5))  # Adjust the height as needed


def output_name(name):
    pass


def block_table_1(data):
    table_data = [
        [data[0], data[2]],
        [data[1]],
    ]

    table = Table(table_data)
    table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (0, 0), 'TOP')
    ]))
    flowables.append(table)


def data_table_1(processed):
    # Create a list to store the table data
    table_data = [
        ["", Paragraph("<u>Total</u>", style=ParagraphStyle(name='Total')),
         Paragraph("<u>Not Old</u>", style=ParagraphStyle(name='Total'))],
        [Paragraph("<u># créditos totales</u>:"), str(processed['Creditos Totales']), str(processed['Creditos Totales '
                                                                                                    '- Not Old'])],
        [Paragraph("<u># créditos activos</u>:"), str(processed['Creditos Activos']), str(processed['Creditos Activos '
                                                                                                    '- Not Old'])],
        [Paragraph("<u># créditos atrasados</u>:"), str(processed['Creditos Atrasados']),
         str(processed['Creditos Atrasados - Not Old'])],
        [Paragraph(f"<u>- filas {str(processed['Filas Atrasadas'])}</u>")],
        [Paragraph("<u>Saldo actual</u>:"), f"${str(processed['Saldo Actual'])}",
         f"${str(processed['Saldo Actual - Not Old'])}"],
        [Paragraph("<u>Pago mensual actual</u>:"), f"${str(processed['Pago Mensual Actual'])}",
         f"${str(processed['Pago Mensual Actual - Not Old'])}"],
    ]

    # Create the table and set its style
    table = Table(table_data, colWidths=[110, 45, 45], rowHeights=12)
    table.setStyle(TableStyle([
        ('LINEBELOW', (0, 5), (-1, 5), 1, colors.black),
        ('ALIGN', (0, 0), (-1, 3), 'LEFT'),
        ('ALIGN', (0, 5), (-1, -1), 'LEFT'),
        ('ALIGN', (0, 4), (0, 4), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black)
    ]))

    return table


def data_table_2(processed):
    # Create a list to store the table data
    table_data = [
        [Paragraph("<u>Periodo más antiguo</u>:"), str(processed['Periodo Mas Antiguo'])],

        [Paragraph("<u>Saldo más grande (est)</u>:"), str(processed['Saldo mas grande']),
         f"fila({str(processed['Saldo mas grande - Row'])})"],

        [Paragraph("<u>Pago mens mayor (est)</u>:"), f"${str(processed['Pagos mens mayor'])}",
         f"fila({str(processed['Pagos mens mayor - Row'])})"],

        [Paragraph("<u># consultas (ult. 12 meses)</u>:"), str(processed['Consultas Ult 12 Meses'])],

        [Paragraph("<u># consultas (ult. 24 meses)</u>:"), str(processed['Consultas Ult 24 Meses'])]
    ]

    # Create the table and set its style
    table = Table(table_data, colWidths=[150, 45, 45], rowHeights=12)
    table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black)
    ]))

    # Create a KeepInFrame object and add your table to it
    return table


def bar_chart_1(processed):
    # Create a Drawing object to hold the chart
    drawing = Drawing(100, 130)

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
    chart.categoryAxis.visible = False
    chart.valueAxis.visible = False
    # Set the labels for the x-axis
    chart.height = 130
    chart.width = 70

    # Add the chart to the drawing
    drawing.add(chart)

    return drawing


# Extract the data from Reader.py and process it in Processor.py
extracted_data = Reader.extract_data()
general = extracted_data.general_information
clean_records = Processor.clean_data(extracted_data.transactions)
cleaned_inquiries = Processor.clean_inquiries(extracted_data.inquiries)
processed_data = Processor.calculate_data(general, clean_records, cleaned_inquiries)

output_title()
block_table_1([data_table_1(processed_data), data_table_2(processed_data), bar_chart_1(processed_data)])

# Create a PDF document
doc = SimpleDocTemplate("testy.pdf", pagesize=letter, leftMargin=18, rightMargin=18)

# Build the document with the flowables
doc.build(flowables)
