import asyncio
import multiprocessing
from functools import partial
from spacy.training import loop
from dataframe_processing import process_data


async def process_async(pdf_files, output_folder):
    # Initialize a process pool
    pool = multiprocessing.Pool(processes=4)

    # Initialize a list to hold the tasks
    tasks = []

    # Create a loop to go through each pdf file
    for pdf_file in pdf_files:
        # Use the pool to read and process the PDF data
        task = loop.run_in_executor(None, partial(process_data, pdf_file))
        tasks.append(task)

    # Wait for all tasks to complete
    results = await asyncio.gather(*tasks)

    return results
