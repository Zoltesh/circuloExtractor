"""
Data processing and concurrent operations
"""

import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from Processing_Functions import (  # import the functions from the new file
    extract_and_process_pdf,
    create_output_pdf,
)


def process_all_pdfs(in_folder: str, out_folder: str):
    with ThreadPoolExecutor() as executor:
        futures = []

        print("Processing PDFs in folder:", in_folder)
        files_in_folder = os.listdir(in_folder)
        print("Files in folder:", files_in_folder)
        counter = 0

        for pdf_file in files_in_folder:  # Change the variable name here
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
                rfc, pdf_data = future.result()
                output_path = Path(out_folder) / f"{rfc}.pdf"
                print(pdf_data, '\n', output_path)

                # Call the create_output_pdf() function with the extracted data and output path
                create_output_pdf(pdf_data, str(output_path))

            except Exception as e:
                print(f"An error occurred: {e}")
