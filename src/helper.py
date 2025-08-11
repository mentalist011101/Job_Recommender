import fitz
import os
from openai import OPENAI
from dotenv import load_dotenv
from google import genai



def extract_text_from_pdf(uploaded_file):
    "Extract text from the uploaded fileand return str"
    text = ""
    try:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page in doc:
                text += page.get_text()
        # with fitz.open(uploaded_file) as doc:
        #     for page in doc:
        #         text += page.get_text()
    except Exception as e:
        print(f"Erreur lors du chargement :{e}")
    return text

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

client = genai.Client()

def ask_llm(prompt, max_token=500):
    "send a prompt to a llm"
    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
        )
    #print(response.text)
    # response = client.chat.completions.create(
    #       model = "gtp-4o",
    #       messages = [{
    #            "role":"user",
    #            "content": prompt
    #       }],
    #       temperature=0.5,
    #       max_token = max_token
    #  )
    return response.text


