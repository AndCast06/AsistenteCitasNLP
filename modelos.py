from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_openai import ChatOpenAI
from credenciales import Credenciales
from langchain_community.llms import HuggingFaceEndpoint


class Modelos:
    def __init__(self):
        credenciales = Credenciales()
        
        self.embeddings = HuggingFaceInferenceAPIEmbeddings(
            api_key=credenciales.get_huggingface_key(),
            model_name="sentence-transformers/all-MiniLM-l6-v2"
        )

        self.llm= ChatOpenAI(temperature=0, model="gpt-4o",api_key="")

    def get_embeddings(self):
        return self.embeddings

    def get_llm(self):
        return self.llm
    

