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
    'Quincenal': 15,
    'Mensual': 30,
    'Bimestral': 60
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
