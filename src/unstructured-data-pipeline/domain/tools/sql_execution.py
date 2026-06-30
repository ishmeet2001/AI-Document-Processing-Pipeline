from langchain.tools import tool
import sqlite3
from config import GENERATED_SCHEMA_PATH

@tool
def manipulating_DBTable(query:str,path:str=GENERATED_SCHEMA_PATH)->str:
    """
    Executes SQL statements to create tables, insert, or update data.
    Returns a success/failure message.
    """
    import time
    max_retries = 3
    for attempt in range(max_retries):
        try:
            connection_object = sqlite3.connect(path)
            cur = connection_object.cursor()
            with connection_object:
                cur.executescript(query)
            return "SQL executed successfully"
        except sqlite3.Error as e:
            if attempt == max_retries - 1:
                return f"SQL execution failed after {max_retries} attempts: {e}"
            time.sleep(1)
        finally:
            connection_object.close()
