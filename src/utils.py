import os

def split_wordlist(wordlist_path, num_chunks):
    """
    Split a wordlist into multiple chunks for parallel processing.
    :param wordlist_path: Path to the wordlist file.
    :param num_chunks: Number of chunks to create.
    :return: List of chunk file paths.
    """
    chunk_paths = []
    with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as file:
        lines = file.readlines()
        chunk_size = len(lines) // num_chunks

        for i in range(num_chunks):
            chunk_path = f"{wordlist_path}.chunk{i}"
            with open(chunk_path, 'w') as chunk_file:
                start = i * chunk_size
                end = start + chunk_size if i < num_chunks - 1 else len(lines)
                chunk_file.writelines(lines[start:end])
            chunk_paths.append(chunk_path)

    return chunk_paths

def cleanup_temp_files(file_paths):
    """
    Delete temporary files created during processing.
    :param file_paths: List of file paths to delete.
    """
    for path in file_paths:
        if os.path.exists(path):
            os.remove(path)

def assemble_results(result_queue):
    """
    Collect results from the multiprocessing queue.
    :param result_queue: Queue containing results from GPU processes.
    :return: Cracked password if found, None otherwise.
    """
    while not result_queue.empty():
        result = result_queue.get()
        if result is not None:
            return result
    return None
