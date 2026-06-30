import os 
from domain.validators.file_naming import validate_empty_path,validate_file_type,validate_file_existence
from typing import Set
from concurrent.futures import ThreadPoolExecutor
from config import OPTIMAL_NUMBER_THREADS,FILE_TYPES

def Thread_Validation_Function(path: str) -> str | None:
    # validating the file paths
    if validate_empty_path(path) and validate_file_type(path) and validate_file_existence(path):
        return path
    return None

def Thread_File_Reader(path: str) -> str | None:
    # reading the content of file
    try:
        with open(path, "r") as file:
            return file.read()
    except Exception as e:
        print(f"Failed to read Content of file:{path}: {e}")
        return None

def read_files(file_paths: list[str]) -> Set[str]:
    # Validate the files in parallel and filter out invalid/None paths
    with ThreadPoolExecutor(max_workers=OPTIMAL_NUMBER_THREADS) as e:
        validation_results = e.map(Thread_Validation_Function, file_paths)
    
    valid_files = {path for path in validation_results if path is not None}
    
    # Read the valid files in parallel
    with ThreadPoolExecutor(max_workers=OPTIMAL_NUMBER_THREADS) as e:
        reading_results = e.map(Thread_File_Reader, valid_files)
        
    return {content for content in reading_results if content is not None}

    