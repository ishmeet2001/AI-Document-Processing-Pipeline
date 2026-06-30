from dotenv import load_dotenv
import os

load_dotenv(".env.local")

GENERATED_SCHEMA_PATH=os.getenv("FILES_STORAGE")
FILE_TYPES=os.getenv("FILE_TYPES_ALLOWED")

OPTIMAL_NUMBER_THREADS=min(32,(os.cpu_count() or 1)+4)

COMMAND=os.getenv("PROCESS_COMMAND")

GEMINI_API_KEY=os.getenv("GOOGLE_GEMINI_API_KEY")