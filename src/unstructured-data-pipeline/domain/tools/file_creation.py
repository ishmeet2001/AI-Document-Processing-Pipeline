from langchain.tools import tool
import os 
from config import GENERATED_SCHEMA_PATH

@tool
def check_DBfile_existence(path:str=GENERATED_SCHEMA_PATH)->bool:
    """
    Check if the file exist or not
    return Exists/Missing
    """
    if os.path.isfile(path):
        return True
    return False

@tool
def db_file_creation(path:str=GENERATED_SCHEMA_PATH)->str:
    """
    Create a new Database file
    Returns Success/Failure
    """
    try:
        with open(path,"w") as file:
            return "Database File Created Successfully"
    except Exception as e:
        return f"Failed to create database file: {e}"