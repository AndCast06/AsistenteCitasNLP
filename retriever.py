from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from credenciales import Credenciales
from loaddb import AbrirChromaDB
from langchain_openai import ChatOpenAI
import os
from creardb import CreacionDB

cred = Credenciales()
api_key = cred.get_huggingface_key()
api_key_open = ""
os.environ["OPENAI_API_KEY"] = api_key_open
db_directory = "./ChromaDB"

class ConversationalRetriever:
    def __init__(self, collection_name):
        abrir_db = AbrirChromaDB(api_key, db_directory=db_directory)
        vector_store = abrir_db.load_chroma_collection(collection_name)  # Cargar la colección especificada
        self.retriever = vector_store.as_retriever(search_type="similarity")
        
        self.llm = ChatOpenAI(temperature=0, model="gpt-4o")

    def format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def execute_query(self, question: str) -> str:
        template = """
            Responda la pregunta según el contexto proporcionado.
        \n\n
        contexto:\n {context}?\n
        pregunta: \n{question}\n
        Respuesta:
        """
        custom_rag_prompt = PromptTemplate.from_template(template)
        rag_chain = (
            {"context": self.retriever | self.format_docs, "question": RunnablePassthrough()}
            | custom_rag_prompt
            | self.llm
            | StrOutputParser()
        )
        answer = rag_chain.invoke(question)
        return answer

    def chat(self, pregunta):
        respuesta = self.execute_query(pregunta)
        return respuesta


#collection_name = "profesionales"  
#chatbot = ConversationalRetriever(collection_name)
#chatbot.chat("Devuelve solo el id de la Dra Carmen Jiménez")
#abrir_db = AbrirChromaDB(api_key, db_directory=db_directory)
#collection_name = "disponibilidad_base"  
#vector_store = abrir_db.load_chroma_collection(collection_name).get()["ids"]
#print(vector_store)

