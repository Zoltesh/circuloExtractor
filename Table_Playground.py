import camelot
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt

matplotlib.use('TkAgg')  # or 'Qt5Agg'

# Set pandas display options
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)

# Specify the path
pathy = 'Z:\\Code\\Credit Report Summary\\New Example Input\\Example input.pdf'

# Read the PDF file, specifying the page number
tables = camelot.read_pdf(pathy, pages='2', flavor='lattice', line_scale=100)

# Plotting
camelot.plot(tables[0], kind='grid')
plt.show()

# Define positions of values within each record
positions = {
    # Row 1
    'Frequency': (0, 0),
    'ID': (0, 1),
    'Responsabilidad': (0, 3),
    'Credito': (0, 4),
    'Otorgante': (0, 5),
    'Plazo': (0, 6),
    'EstatusCAN': (0, 7),
    'Limite': (0, 8),
    'Aprobado': (0, 9),
    'Actual': (0, 10),
    'Vencido': (0, 11),
    'A pagar': (0, 12),
    'Reporte': (0, 13),
    'Apertura': (0, 14),
    'Cierre': (0, 15),
    'Pago': (0, 16),
    'Atraso': (0, 17),
    'Monto': (0, 18),
    'Fecha': (0, 19),

    # Row 2
    'Situacion': (1, 17),

    # Row 3
    'Historial': (2, 6)
}

for i, table in enumerate(tables):
    # Iterate over the rows of the DataFrame in steps of 3 (assuming each record is 3 rows long)
    records = []
    for start_row in range(5, len(table.df), 3):
        record = {}
        for key, (row_offset, col) in positions.items():
            record[key] = table.df.iloc[start_row + row_offset, col]
        records.append(record)

    # Now 'records' is a list of dictionaries, each representing a record from the table
    for record in records:
        print(record)

    # Export to Excel
    table.df.to_excel(f'table_{i}.xlsx', index=False)
