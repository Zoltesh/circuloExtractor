# Payment_History_Processor.py

import pdfplumber
import pandas as pd


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
