# Payment_History_Processor.py

# Payment_History_Processor.py

import re
import pandas as pd


def extract_payment_history(text):
    # Define a regex pattern to find the table in the text
    table_pattern = re.compile(r"Descripción, Montos.*?Periodos\] Últimos 24", re.DOTALL)
    table_match = table_pattern.search(text)

    if table_match:
        # Extract the table data as a list of rows
        table_data = table_match.group().split("\n")

        # Convert the table data into a DataFrame
        payment_history_df = pd.DataFrame([row.split(",") for row in table_data])

        return payment_history_df
    else:
        return None


def process_payment_history(table):
    unique_indices = []

    # Function to find index of a cell containing frequency value
    def find_frequency_index(row, frequencies):
        for idx, cell in enumerate(row):
            if cell in frequencies:
                return idx
        return -1

    frequencies = ["Semanal", "Catorcenal", "Mensual"]

    for row in table:
        freq_idx = find_frequency_index(row, frequencies)

        # If the frequency is found and there is a valid unique index to the right
        if freq_idx != -1 and freq_idx + 2 < len(row):
            try:
                index = int(row[freq_idx + 2])
                unique_indices.append(index)
            except ValueError:
                # The cell does not contain an integer, so move on to the next row
                continue

    df = pd.DataFrame(unique_indices, columns=["#"])
    return df

