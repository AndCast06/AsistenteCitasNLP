# credenciales.py

import os
from dotenv import load_dotenv

class Credenciales:
    def __init__(self):
        load_dotenv()
        self.api_key_openai = os.getenv("OPENAI_KEY")
        self.api_key_huggingface = os.getenv("HUGGINGFACEHUB_API_TOKEN")

    def get_openai_key(self):
        return self.api_key_openai

    def get_huggingface_key(self):
        return ""





