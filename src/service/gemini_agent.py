import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

client = genai.GenerativeModel(model_name="gemini-2.0-flash")

def generar_recomendacion(prompt: str):
    response = client.generate_content(
        contents=prompt,
        generation_config={
            "temperature": 1,
            "top_p": 1,
            "max_output_tokens": 1024,
        }
    )
    return response.text
