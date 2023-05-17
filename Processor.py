import decimal
import datetime
import Reader
import pandas as pd
from Constants import SPANISH_TO_ENGLISH_MONTHS, SPANISH_TO_ENGLISH_MONTHS_FULL, TIME_INTERVALS


def handle_historial(code_string, target_length):
    substrings = code_string.split('.')
    while len(substrings) < target_length:
        remaining = target_length - len(substrings)
        substrings += code_string.split('.', remaining - 1)[:remaining]
    return substrings[:target_length]


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


def clean_data(records):
    for record in records:
        # Remove spaces from ID
        record['ID'] = record['ID'].replace(' ', '')

        # Replace '\n' with space in 'Responsabilidad', 'Credito', and 'Otorgante'
        record['Responsabilidad'] = record['Responsabilidad'].replace('\n', ' ')
        record['Credito'] = record['Credito'].replace('\n', ' ')
        record['Otorgante'] = record['Otorgante'].replace('\n', ' ')

        # Convert currency columns to Decimal
        for col in ['Limite', 'Aprobado', 'Actual', 'Vencido', 'A pagar']:
            try:
                # Remove currency symbol and commas, and convert to Decimal
                record[col] = decimal.Decimal(record[col].replace('$', '').replace(',', ''))
            except decimal.InvalidOperation:
                # Handle invalid currency values by assigning None
                record[col] = None

        # Convert 'Reporte', 'Apertura', 'Cierre', 'Pago', 'Fecha' to datetime
        for col in ['Reporte', 'Apertura', 'Cierre', 'Pago', 'Fecha']:
            # Replace Spanish month abbreviations with English ones
            for es_month, en_month in SPANISH_TO_ENGLISH_MONTHS.items():
                record[col] = record[col].replace(es_month, en_month)

            # Check for empty date values
            if record[col]:
                try:
                    # Convert to datetime
                    record[col] = datetime.datetime.strptime(record[col], '%d/%b/%y')
                except ValueError:
                    # Handle invalid date values by assigning None
                    record[col] = None

        # Split Historial into a list of substrings
        code_string = record['Historial']
        target_length = 24
        substrings = handle_historial(code_string, target_length)
        record['Historial'] = substrings
    return records


def calculate_total_credits_not_old(consult_date, df_cleaned_records):
    total = 0
    threshold = pd.Timedelta(days=365.25 / 12 * 2 * 12)

    for index, record in df_cleaned_records.iterrows():
        if (consult_date - record['Apertura']) > threshold:
            continue
        else:
            total += 1

    return total


def calculate_total_credits_late(df_cleaned_records):
    total = 0
    rows = []
    for _, record in df_cleaned_records.iterrows():
        actual_result = 1 if record['Actual'] > decimal.Decimal('0') else 0
        historial_result = 0 if record['Historial'][0] in ('V', '', '-') else 1
        if historial_result * actual_result == 1:
            total += 1
            rows.append(record['ID'])
    return total, rows


def calculate_monthly_amount(M, O, J):
    try:
        monthly_amount = min(M, O * 30 / J)
    except decimal.InvalidOperation:
        monthly_amount = decimal.Decimal('')
    return monthly_amount


def calculate_total_monthly_amount(df_cleaned_records):
    total_amount = decimal.Decimal(0)
    for index, row in df_cleaned_records.iterrows():
        M = row['Actual']
        O = row['A pagar']
        J = TIME_INTERVALS[row['Frequency']]
        monthly_amount = calculate_monthly_amount(M, O, J)
        total_amount += monthly_amount
    return total_amount


def calculate_data(cleaned_records):
    # General Data
    general = extracted_data.general_information
    new_fecha = clean_fecha_consulta(general['Fecha de consulta'])
    name = general['Nombre (s)'] + ' ' + general['Apellido Paterno'] + ' ' + general['Apellido Materno']

    calculated_dict = {}
    df_cleaned_records = pd.DataFrame(cleaned_records)
    total_credits = len(df_cleaned_records)
    total_credits_not_old = calculate_total_credits_not_old(new_fecha, df_cleaned_records)
    total_credits_active = len(df_cleaned_records[df_cleaned_records['Actual'] > 0])
    total_credits_late, late_rows = calculate_total_credits_late(df_cleaned_records)
    current_balance = df_cleaned_records['Actual'].sum()
    current_monthly_payment = calculate_total_monthly_amount(df_cleaned_records=df_cleaned_records)

    calculated_dict['Creditos Totales'] = total_credits
    calculated_dict['Creditos Totales - Not Old'] = total_credits_not_old
    calculated_dict['Creditos Activos'] = total_credits_active
    calculated_dict['Creditos Atrasados'] = total_credits_late
    calculated_dict['Filas Atrasadas'] = late_rows
    calculated_dict['Saldo Actual'] = current_balance
    calculated_dict['Pago Mensual Actual'] = current_monthly_payment
    print(total_credits_not_old)


# Extract the data
extracted_data = Reader.extract_data()

# Clean the data
clean_records = clean_data(extracted_data.transactions)

# Process the cleaned records
"""for clean in clean_records:
    # Perform further processing or calculations on the clean records
    # Example: print the cleaned record
    print(clean)"""
calculate_data(clean_records)
