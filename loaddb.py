from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_community.vectorstores import Chroma

class AbrirChromaDB:
    def __init__(self, api_key, db_directory):
        self.embeddings = HuggingFaceInferenceAPIEmbeddings(
            api_key=api_key, model_name="sentence-transformers/all-MiniLM-l6-v2"
        )
        self.db_directory = db_directory

    def load_chroma_db(self):
        # Cargar toda la base de datos Chroma
        vector_store = Chroma(persist_directory=self.db_directory, embedding_function=self.embeddings)
        return vector_store

    def load_chroma_collection(self, collection_name):
        # Cargar una colección específica en Chroma
        vector_store = Chroma(
            collection_name=collection_name,
            persist_directory=self.db_directory,
            embedding_function=self.embeddings
        )
        return vector_store





