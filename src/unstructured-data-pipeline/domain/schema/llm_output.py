from pydantic import BaseModel
from typing import List

class response_output(BaseModel):
    sql_statements:str