from langchain_google_genai import ChatGoogleGenerativeAI
from config import GEMINI_API_KEY

def create_gemini_instance(model_name:str="gemini-2.5-flash-lite",temperature:float=0):
    model=ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=GEMINI_API_KEY,
        temperature=temperature,
    )
    return model