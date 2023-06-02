import multiprocessing
from pathlib import Path
from dataframe_processing import process_data


def process_files(input_folder, output_folder):
    # Process all PDF files in the input folder
    pdf_files = []
    for file in Path(input_folder).iterdir():
        print(f"File: {file}, type: {type(file)}, suffix: {file.suffix}, type of suffix: {type(file.suffix)}")
        if file.suffix.lower() == '.pdf' and not file.name.startswith('~'):
            pdf_files.append(file)
    # Create a multiprocessing pool
    pool = multiprocessing.Pool(processes=4)

    # Process each file using the multiprocessing pool
    results = []
    for pdf_file in pdf_files:
        result = pool.apply_async(process_data, args=(pdf_file,))
        results.append(result)

    # Close the pool and wait for all processes to complete
    pool.close()
    pool.join()

    # Extract results from multiprocessing
    extracted_data_list = [result.get() for result in results]

    return extracted_data_list
