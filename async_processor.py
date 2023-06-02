import asyncio
import concurrent.futures
from dataframe_processing import process_data


async def process_async(pdf_files):
    # Initialize a ProcessPoolExecutor
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        # Initialize a list to hold the tasks
        tasks = []

        # Create a loop to go through each pdf file
        for pdf_file in pdf_files:
            # Offload the processing to the executor
            task = loop.run_in_executor(executor, process_data, pdf_file)
            tasks.append(task)

        # Wait for all tasks to complete
        async_results = await asyncio.gather(*tasks)

    return async_results


# To run the above coroutine:
loop = asyncio.get_event_loop()
pdf_files_list = []  # this should be your list of pdf files
results = loop.run_until_complete(process_async(pdf_files_list))
