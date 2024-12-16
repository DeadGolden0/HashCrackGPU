import pytest
from utils import split_wordlist, cleanup_temp_files, assemble_results
import os

def test_split_wordlist():
    wordlist_path = "test_wordlist.txt"
    with open(wordlist_path, 'w') as file:
        file.writelines([f"password{i}\n" for i in range(10)])

    chunks = split_wordlist(wordlist_path, 2)
    assert len(chunks) == 2

    cleanup_temp_files(chunks)
    os.remove(wordlist_path)

def test_cleanup_temp_files():
    temp_files = ["temp1.txt", "temp2.txt"]
    for file in temp_files:
        with open(file, 'w') as f:
            f.write("test")
    cleanup_temp_files(temp_files)
    for file in temp_files:
        assert not os.path.exists(file)
