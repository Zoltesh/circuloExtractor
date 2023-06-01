from Reader import extract_data
from Writer import process_extracted_data

from Reader import extract_data


def process_file(input_file, output_folder):
    extracted_data = extract_data(str(input_file))
    return input_file, extracted_data
