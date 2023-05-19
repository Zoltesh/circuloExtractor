# A dictionary mapping Spanish month abbreviations to English ones
import decimal

SPANISH_TO_ENGLISH_MONTHS = {
    'ENE': 'JAN', 'FEB': 'FEB', 'MAR': 'MAR', 'ABR': 'APR',
    'MAY': 'MAY', 'JUN': 'JUN', 'JUL': 'JUL', 'AGO': 'AUG',
    'SEP': 'SEP', 'OCT': 'OCT', 'NOV': 'NOV', 'DIC': 'DEC'
}

# Map full month word to 3 letter english
SPANISH_TO_ENGLISH_MONTHS_FULL = {
            'Enero': 'Jan',
            'Febrero': 'Feb',
            'Marzo': 'Mar',
            'Abril': 'Apr',
            'Mayo': 'May',
            'Junio': 'Jun',
            'Julio': 'Jul',
            'Agosto': 'Aug',
            'Septiembre': 'Sep',
            'Octubre': 'Oct',
            'Noviembre': 'Nov',
            'Diciembre': 'Dec'
        }

TIME_INTERVALS = {
    'Semanal': 7,
    'Catorcenal': 14,
    'Mensual': 30
}

# These are the local positions of the values in a credit record
POSITIONS = {
    # Row 1
    'Frequency': (1, 0),
    'ID': (1, 2),
    'Responsabilidad': (1, 3),
    'Credito': (1, 4),
    'Otorgante': (1, 5),
    'Plazo': (1, 6),
    'EstatusCAN': (1, 7),
    'Limite': (1, 8),
    'Aprobado': (1, 9),
    'Actual': (1, 10),
    'Vencido': (1, 11),
    'A pagar': (1, 12),
    'Reporte': (1, 13),
    'Apertura': (1, 14),
    'Cierre': (1, 15),
    'Pago': (1, 16),
    'Atraso': (1, 17),
    'Monto': (1, 18),
    'Fecha': (1, 19),

    # Row 2
    'Situacion': (2, 17),

    # Row 3
    'Historial': (3, 6)
}

# The local positions for Consultas Realizadas
INQUIRY_POSITIONS = {
    'Fecha de Consulta': (1, 0),
    'Otorgante': (1, 1),
    'Tipo de Crédito': (1, 2),
    'Monto': (1, 3),
    'Moneda': (1, 4)
}

ELEVATE_SCORING_ALGORITHM = {
    # First value in list is FICO Weight, second is Elevate Weight
    'Payment History': [decimal.Decimal('0.35'), decimal.Decimal('0.46')],
    'Amounts Owed': [decimal.Decimal('0.30'), decimal.Decimal('0.24')],
    'Length of Credit': [decimal.Decimal('0.15'), decimal.Decimal('0.10')],
    'New Credit': [decimal.Decimal('0.10'), decimal.Decimal('0.05')],
    'Types of Credit (Credit Mix)': [decimal.Decimal('0.10'), decimal.Decimal('0.05')],
    'Inquiries': [decimal.Decimal('0.00'), decimal.Decimal('0.04')],
    'Largest Loan / Largest Payment': [decimal.Decimal('0.00'), decimal.Decimal('0.06')],
    'Cobranza / Quebranto Penalties': [decimal.Decimal('0.00'), decimal.Decimal('0.00')]
}

GRUPO_SOLIDARIO = decimal.Decimal('0.33')
WEEKLY_LOAN_ADJUSTMENT = decimal.Decimal('0.50')
ON_TIME_VS_DELINQUENT = decimal.Decimal('0.31')
DEPTH_PAYMENT_HISTORY = decimal.Decimal('0.15')
HIPOTECA = decimal.Decimal('0.15')
ALL_OTHER = decimal.Decimal('1')