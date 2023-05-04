# Processor.py

import os
import pdfplumber
import pandas as pd
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from Processing_Functions import (
    extract_and_process_pdf,
    create_output_pdf,
)
import Payment_History_Processor


def extract_payment_history_data(table):
    # Call the process_payment_history function from Payment_History_Processor.py
    payment_history_df = Payment_History_Processor.process_payment_history(table)
    return payment_history_df


def process_all_pdfs(in_folder: str, out_folder: str):
    with ThreadPoolExecutor() as executor:
        futures = []

        print("Processing PDFs in folder:", in_folder)
        files_in_folder = os.listdir(in_folder)
        print("Files in folder:", files_in_folder)
        counter = 0

        for pdf_file in files_in_folder:
            if pdf_file.endswith(".pdf"):
                counter += 1
                print(f"Processing file {counter}: {pdf_file}")
                input_path = Path(in_folder) / pdf_file
                output_path = Path(out_folder) / pdf_file

                # Submit the task to extract and process the PDF into a DataFrame
                future = executor.submit(extract_and_process_pdf, str(input_path))
                future.output_path = str(output_path)
                futures.append(future)

        for future in as_completed(futures):
            try:
                rfc, general_data_df = future.result()
                output_path = Path(out_folder) / f"{rfc}.pdf"
                print(general_data_df, '\n', output_path)

                # Read the input PDF file and extract the payment history table
                with pdfplumber.open(input_path) as pdf:
                    # You may need to adjust the table extraction logic
                    payment_history_table = pdf.pages[0].extract_table()

                # Process the payment history table and get the DataFrame
                payment_history_df = extract_payment_history_data(payment_history_table)

                # Concatenate the DataFrames (general_data_df and payment_history_df) before creating the output PDF
                final_df = pd.concat([general_data_df, payment_history_df], axis=1)

                # Call the create_output_pdf() function with the final DataFrame and output path
                create_output_pdf(final_df, str(output_path))

            except Exception as e:
                print(f"An error occurred: {e}")
