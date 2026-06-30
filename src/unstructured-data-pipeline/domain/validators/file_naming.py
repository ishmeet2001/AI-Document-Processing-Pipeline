import os 
from config import FILE_TYPES

def validate_empty_path(path:str)->bool:
    if len(path)==0:
        return False
    return True
    
def validate_file_type(path:str)->bool:
    chunks=path.split(".")
    if chunks[-1]==FILE_TYPES and len(chunks)!=1:
        return True
    else:
        print(f'only .txt files are supported:{path}')
        return False
    
def validate_file_existence(path:str)->bool:
    if os.path.isfile(path):
        return True
    else:
        print(f'file does not exist. Invalid Path:{path}')
        return False
