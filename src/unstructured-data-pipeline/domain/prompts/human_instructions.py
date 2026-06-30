from langchain_core.prompts import HumanMessagePromptTemplate

human_template = HumanMessagePromptTemplate.from_template(
    "Here is the data that needs to be processed and stored in SQLite.\n\n"

    "### Input Content\n"
    "{content}\n\n"

    "### Output Database Path (optional)\n"
    "{output_db_path}\n\n"

    "Instructions:\n"
    "- If an output database path is provided, use it.\n"
    "- If no output database path is provided, proceed without assuming a path and "
    "allow the database tools to handle the default location."
)