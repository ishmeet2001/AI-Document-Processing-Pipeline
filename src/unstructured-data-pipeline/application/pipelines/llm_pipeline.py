from domain.prompts.llm_instructions import template
from domain.schema.invoice import Invoice,ItemDetails
from domain.schema.llm_output import response_output
from domain.tools.file_creation import db_file_creation,check_DBfile_existence
from domain.tools.sql_execution import manipulating_DBTable
from infrastructure.llm_providers.gemini_provider import create_gemini_instance
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langgraph.checkpoint.memory import InMemorySaver
from pydantic import BaseModel
from typing import Type
import json

checkPointer=InMemorySaver()

def create_agent_instance(primary_schema: Type[BaseModel] = Invoice, foreign_schema: Type[BaseModel] = ItemDetails):
    formatted_template=format_template(primary_schema, foreign_schema)
    agent=create_agent(
        model=create_gemini_instance(),
        system_prompt=formatted_template,
        tools=[db_file_creation,check_DBfile_existence,manipulating_DBTable],
        response_format=ToolStrategy(response_output),
        checkpointer=checkPointer,
    )

    return agent


def format_template(main_schema: Type[BaseModel], foreign_schema: Type[BaseModel])->str:

    formatted_template=template.format(
        primary_schema=json.dumps(main_schema.model_json_schema(),indent=2),
        foreign_schema=json.dumps(foreign_schema.model_json_schema(),indent=2)
    )
    return formatted_template