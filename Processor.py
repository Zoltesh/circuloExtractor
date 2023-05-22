import decimal
import datetime
import Reader
import pandas as pd
from Constants import SPANISH_TO_ENGLISH_MONTHS, SPANISH_TO_ENGLISH_MONTHS_FULL, TIME_INTERVALS, GRUPO_SOLIDARIO, \
    WEEKLY_LOAN_ADJUSTMENT, HIPOTECA, ALL_OTHER


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
        for col in ['Limite', 'Aprobado', 'Actual', 'Vencido', 'A pagar', 'Plazo']:
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


def clean_inquiries(inquiries):
    """
    Cleans the inquiries data.

    Args:
        inquiries (list): The list of inquiries to clean.

    Returns:
        list: The cleaned inquiries.

    """
    cleaned_inquiries = []

    for inquiry in inquiries:
        cleaned_inquiry = {}

        # Clean 'Fecha de Consulta'
        fecha_consulta = inquiry['Fecha de Consulta']
        for es_month, en_month in SPANISH_TO_ENGLISH_MONTHS.items():
            fecha_consulta = fecha_consulta.replace(es_month, en_month)
        cleaned_inquiry['Fecha de Consulta'] = datetime.datetime.strptime(fecha_consulta, '%d/%b/%y')

        # Clean 'Otorgante', 'Tipo de Crédito', and 'Moneda'
        cleaned_inquiry['Otorgante'] = inquiry['Otorgante']
        cleaned_inquiry['Tipo de Credito'] = inquiry['Tipo de Crédito']
        cleaned_inquiry['Moneda'] = inquiry['Moneda']

        # Clean 'Monto'
        monto = inquiry['Monto']
        try:
            monto_decimal = decimal.Decimal(monto.replace('$', '').replace(',', ''))
            cleaned_inquiry['Monto'] = monto_decimal.quantize(decimal.Decimal('1'))
        except decimal.InvalidOperation:
            cleaned_inquiry['Monto'] = None

        cleaned_inquiries.append(cleaned_inquiry)

    return cleaned_inquiries


def calculate_total_credits_not_old(consult_date, df_cleaned_records):
    total = 0
    threshold = pd.Timedelta(days=365.25 / 12 * 2 * 12)

    for index, record in df_cleaned_records.iterrows():
        if (consult_date - record['Apertura']) > threshold:
            continue
        elif record['Responsabilidad']:
            total += 1

    return total


def calculate_total_credits_active_not_old(consult_date, df_cleaned_records):
    total = 0
    threshold = pd.Timedelta(days=365.25 / 12 * 2 * 12)

    for index, record in df_cleaned_records.iterrows():
        if (consult_date - record['Apertura']) > threshold:
            continue
        elif record['Actual'] > decimal.Decimal('0'):
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


def calculate_total_credits_late_not_old(consult_date, df_cleaned_records):
    total = 0
    threshold = pd.Timedelta(days=365.25 / 12 * 2 * 12)

    for index, record in df_cleaned_records.iterrows():
        actual_result = 1 if record['Actual'] > decimal.Decimal('0') else 0
        historial_result = 0 if record['Historial'][0] in ('V', '', '-') else 1
        if (consult_date - record['Apertura']) > threshold:
            continue
        elif historial_result * actual_result == 1:
            total += 1
    return total


def calculate_current_balance_not_old(consult_date, df_cleaned_records):
    total = decimal.Decimal('0')
    threshold = pd.Timedelta(days=365.25 / 12 * 2 * 12)

    for index, record in df_cleaned_records.iterrows():
        if (consult_date - record['Apertura']) > threshold:
            continue
        else:
            total += record['Actual']

    return total


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


def calculate_total_monthly_amount_not_old(consult_date, df_cleaned_records):
    total = decimal.Decimal('0')
    threshold = pd.Timedelta(days=365.25 / 12 * 2 * 12)

    for index, record in df_cleaned_records.iterrows():
        if (consult_date - record['Apertura']) > threshold:
            continue
        else:
            M = record['Actual']
            O = record['A pagar']
            J = TIME_INTERVALS[record['Frequency']]
            monthly_amount = calculate_monthly_amount(M, O, J)
            total += monthly_amount
    return total


"""
TODO Why does spreadsheet refer all records in iterrows to the first record's frequency instead of the current iteration
"""


def calculate_oldest_period(df_cleaned_records):
    first_period = TIME_INTERVALS[df_cleaned_records.loc[0, 'Frequency']]
    min_date = None

    for index, record in df_cleaned_records.iterrows():
        if not (isinstance(record['Reporte'], datetime.datetime) and isinstance(record['Cierre'], datetime.datetime)):
            continue
        first_date = min(record['Reporte'], record['Cierre'])

        if min_date is None:
            min_date = first_date

        for i, h in enumerate(record['Historial']):
            if h == '-' or not h:
                continue
            current_date = first_date - pd.Timedelta(days=(first_period * i))
            min_date = min(min_date, current_date)

    return min_date


def calculate_monthly_payment(record):
    if record['Responsabilidad'] == 'GRUPO SOLIDARIO':
        monthly = record['Aprobado'] * GRUPO_SOLIDARIO
    elif record['Frequency'] == 'Semanal':
        monthly = record['Aprobado'] * WEEKLY_LOAN_ADJUSTMENT
    else:
        monthly = record['Aprobado']
    return monthly


def calculate_largest_balance(df_cleaned_records):
    largest = decimal.Decimal('0')
    balance = decimal.Decimal('0')
    largest_row = None
    for index, record in df_cleaned_records.iterrows():
        if record['Responsabilidad'] == 'GRUPO SOLIDARIO':
            balance = record['Aprobado'] * GRUPO_SOLIDARIO
        elif record['Frequency'] == 'Semanal':
            balance = record['Aprobado'] * WEEKLY_LOAN_ADJUSTMENT
        else:
            balance = record['Aprobado']
        if balance > largest:  # Check if the current balance is larger than the previous largest
            largest = balance
            largest_row = record['ID']  # Store the ID associated with the largest balance

    return largest, largest_row


def calculate_pmt(rate, term_number, principal):
    # rate * principle
    pmt = (rate * principal) / \
          (decimal.Decimal('1')
           # Subtract (1 + rate)^(-term_number)
           - (
                   (
                           decimal.Decimal('1') + rate
                   ) ** (
                       decimal.Decimal(-abs(term_number))
                   )
           )
           )

    return pmt


def calculate_largest_monthly_payment(df_cleaned_records):
    largest = decimal.Decimal('0')
    largest_row = None
    for index, record in df_cleaned_records.iterrows():
        monthly_payment = calculate_monthly_payment(record=record)
        try:
            days = decimal.Decimal(TIME_INTERVALS[record['Frequency']])
            time_calc = decimal.Decimal('360') / days
            if record['Credito'] == 'HIPOTECA':
                rate = HIPOTECA / time_calc
            else:
                rate = ALL_OTHER / time_calc
            pmt = calculate_pmt(rate=rate,
                                term_number=record['Plazo'],
                                principal=monthly_payment)

            pmt *= (decimal.Decimal('30') / days)
            if pmt > largest:
                largest = pmt
                largest_row = record['ID']

        except Exception:
            largest = decimal.Decimal('0')
    largest = largest.quantize(decimal.Decimal('1'))
    return largest, largest_row


def calculate_inquiries_12_months(consult_date, df_cleaned_inquiries):
    inquiries = decimal.Decimal('0')
    month_diff = pd.Timedelta(days=365.25)
    for index, inquiry in df_cleaned_inquiries.iterrows():
        if consult_date - inquiry['Fecha de Consulta'] < month_diff:
            inquiries += 1
    return inquiries


def calculate_inquiries_24_months(consult_date, df_cleaned_inquiries):
    inquiries = decimal.Decimal('0')
    month_diff = pd.Timedelta(days=730.5)
    for index, inquiry in df_cleaned_inquiries.iterrows():
        if consult_date - inquiry['Fecha de Consulta'] < month_diff:
            inquiries += 1
    return inquiries


"""
TODO: In Reader.py, need to scrape the Consultas Realizadas from the last page of the pdf
def calculate_inquiries_12_months(df_cleaned_records, fecha_buro):
    inquires_12_months = decimal.Decimal('0')
    for index, record in df_cleaned_records.iterrows():
        if (fecha_buro
"""


def calculate_data(general, cleaned_records, cleaned_inquries):
    new_fecha = clean_fecha_consulta(general['Fecha de consulta'])
    first_name = general['Nombre (s)']
    paterno = general['Apellido Paterno']
    materno = general['Apellido Materno']
    rfc = general['RFC']
    name = first_name + ' ' + paterno + ' ' + materno
    output_filename = f'{first_name}_{paterno}_{materno}_{rfc}.pdf'

    calculated_dict = {}
    df_cleaned_records = pd.DataFrame(cleaned_records)
    df_cleaned_inquiries = pd.DataFrame(cleaned_inquries)
    total_credits = len(df_cleaned_records)
    total_credits_not_old = calculate_total_credits_not_old(consult_date=new_fecha,
                                                            df_cleaned_records=df_cleaned_records)
    total_credits_active = len(df_cleaned_records[df_cleaned_records['Actual'] > 0])
    total_credits_active_not_old = calculate_total_credits_active_not_old(consult_date=new_fecha,
                                                                          df_cleaned_records=df_cleaned_records)
    total_credits_late, late_rows = calculate_total_credits_late(df_cleaned_records=df_cleaned_records)
    total_credits_late_not_old = calculate_total_credits_late_not_old(consult_date=new_fecha,
                                                                      df_cleaned_records=df_cleaned_records)
    current_balance = df_cleaned_records['Actual'].sum()
    current_balance_not_old = calculate_current_balance_not_old(consult_date=new_fecha,
                                                                df_cleaned_records=df_cleaned_records)
    current_monthly_payment = calculate_total_monthly_amount(df_cleaned_records=df_cleaned_records)
    current_monthly_payment_not_old = calculate_total_monthly_amount_not_old(consult_date=new_fecha,
                                                                             df_cleaned_records=df_cleaned_records)
    oldest_period = calculate_oldest_period(df_cleaned_records=df_cleaned_records)
    largest_balance, largest_balance_row = calculate_largest_balance(df_cleaned_records=df_cleaned_records)
    largest_monthly_payment, largest_monthly_row = calculate_largest_monthly_payment(
        df_cleaned_records=df_cleaned_records)

    inquiries_12_months = calculate_inquiries_12_months(consult_date=new_fecha,
                                                        df_cleaned_inquiries=df_cleaned_inquiries)
    inquiries_24_months = calculate_inquiries_24_months(consult_date=new_fecha,
                                                        df_cleaned_inquiries=df_cleaned_inquiries)
    print(oldest_period)
    calculated_dict['Output Filename'] = output_filename
    calculated_dict['Nombre'] = name
    calculated_dict['Creditos Totales'] = total_credits
    calculated_dict['Creditos Totales - Not Old'] = total_credits_not_old
    calculated_dict['Creditos Activos'] = total_credits_active
    calculated_dict['Creditos Activos - Not Old'] = total_credits_active_not_old
    calculated_dict['Creditos Atrasados'] = total_credits_late
    calculated_dict['Filas Atrasadas'] = late_rows
    calculated_dict['Creditos Atrasados - Not Old'] = total_credits_late_not_old
    calculated_dict['Saldo Actual'] = current_balance
    calculated_dict['Saldo Actual - Not Old'] = current_balance_not_old
    calculated_dict['Pago Mensual Actual'] = current_monthly_payment
    calculated_dict['Pago Mensual Actual - Not Old'] = current_monthly_payment_not_old
    calculated_dict['Saldo mas grande'] = largest_balance
    calculated_dict['Saldo mas grande - Row'] = largest_balance_row
    calculated_dict['Pagos mens mayor'] = largest_monthly_payment
    calculated_dict['Pagos mens mayor - Row'] = largest_monthly_row
    calculated_dict['Consultas Ult 12 Meses'] = inquiries_12_months
    calculated_dict['Consultas Ult 24 Meses'] = inquiries_24_months

    return calculated_dict


