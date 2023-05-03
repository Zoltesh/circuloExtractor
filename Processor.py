"""
Data processing and concurrent operations
"""

import os
from pathlib import Path
import pandas as pd
import pdfplumber
from concurrent.futures import ThreadPoolExecutor


# Extract data from a single pdf and create a pandas dataframe
def extract_and_process_pdf(input_path: str):
    # Extract text from the input PDF
    text = ''
    with pdfplumber.open(input_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()

    # Process the extracted text and create a pandas DataFrame (data structure)
    # ...
    pass
    """return pd.DataFrame(data)"""


# Create prepare data from a single dataframe to create data visualizations and fill out the output pdf
def process_dataframe(input_path: str, output_path: str):
    # Process each PDF in the input folder
    for file in os.listdir(input_path):
        if file.endswith(".pdf"):
            input_path = os.path.join(input_path, file)

            # Extract text from the input PDF
            text = ''
            with pdfplumber.open(input_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text()
            print(text)

            # Process the extracted text, create data structures, etc.
            # ...

            # Save the output PDF to the output folder
            output_path = os.path.join(output_path, file)
            # ...


def create_data_structure(pdf_data):
    """    # Create a pandas DataFrame with the data from the PDF
    data = {
        'column1': [value1, value2, ...],
        'column2': [value1, value2, ...],
        ...
    }
    df = pd.DataFrame(data)

    # Perform any necessary data processing, calculations, and transformations using pandas functions
    pass"""


def process_all_pdfs(in_folder: str, out_folder: str):
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for file in os.listdir(in_folder):
            if file.endswith(".pdf"):
                input_path = Path(in_folder) / file
                output_path = Path(out_folder) / file

                # Submit the task to extract and process the PDF into a DataFrame
                future = executor.submit(extract_and_process_pdf, str(input_path))
                future.output_path = str(output_path)
                futures.append(future)

        # Process the resulting DataFrames
        for future in futures:
            df = future.result()
            process_dataframe(df, future.output_path)

