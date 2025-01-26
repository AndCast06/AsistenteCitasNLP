import os
from fpdf import FPDF
from conexion import ConexionDB
from credenciales import Credenciales
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

# Crear la carpeta "Informacion" si no existe
os.makedirs("Informacion", exist_ok=True)

# Clase para generar PDFs
def generar_pdfs():
    conexion = ConexionDB()

    try:
        # Generar agenda_base.pdf
        agenda_query = "SELECT paciente_documento, id, profesional_id, dia_semana, hora_inicio, hora_fin FROM agenda"
        agenda_data = conexion.ejecutar_query(agenda_query)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=8)
        pdf.cell(200, 10, ln=True, align='C')

        for row in agenda_data:
            pdf.cell(0, 10, txt=f"paciente: {row[0]}, id: {row[1]}, profesional_id: {row[2]}, dia_semana: {row[3]}, hora_inicio: {row[4]}, hora_fin: {row[5]}", ln=True)

        pdf.output("Informacion/agenda_base.pdf")

        # Generar cups.pdf
        cups_query = "SELECT codigo_cup, procedimiento FROM cups"
        cups_data = conexion.ejecutar_query(cups_query)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=8)
        pdf.cell(200, 10, ln=True, align='C')

        for row in cups_data:
            pdf.cell(0, 10, txt=f"{row[0]}: {row[1]}", ln=True)

        pdf.output("Informacion/Cups.pdf")

        # Generar disponibilidad_base.pdf
        disponibilidad_query = "SELECT id, profesional_id, dia_semana, hora_inicio, hora_fin FROM disponibilidad"
        disponibilidad_data = conexion.ejecutar_query(disponibilidad_query)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=8)
        pdf.cell(200, 10, ln=True, align='C')

        for row in disponibilidad_data:
            pdf.cell(0, 10, txt=f"id: {row[0]}, profesional_id: {row[1]}, dia_semana: {row[2]}, hora_inicio: {row[3]}, hora_fin: {row[4]}", ln=True)

        pdf.output("Informacion/disponibilidad_base.pdf")

        # Generar profesionales.pdf
        profesionales_query = "SELECT id, nombre, especialidad FROM profesionales"
        profesionales_data = conexion.ejecutar_query(profesionales_query)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=8)
        pdf.cell(200, 10, ln=True, align='C')

        for row in profesionales_data:
            pdf.cell(0, 10, txt=f"id: {row[0]}, Nombre: {row[1]}, Especialidad: {row[2]}", ln=True)

        pdf.output("Informacion/profesionales.pdf")

    finally:
        conexion.cerrar_conexion()

# Clase para manejar ChromaDB
class CreacionDB:
    def __init__(self, api_key, db_directory="ChromaDB"):
        self.embeddings = HuggingFaceInferenceAPIEmbeddings(
            api_key=api_key, model_name="sentence-transformers/all-MiniLM-l6-v2"
        )
        self.db_directory = db_directory

    def load_docs(self, file_path):
        loader = PyPDFLoader(file_path)
        return loader.load_and_split()

    def split_text(self, documents):
        text_splitter = RecursiveCharacterTextSplitter(
            separators=["."]
        )
        return text_splitter.split_documents(documents)

    def create_chroma_collection(self, file_path):
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        documents = self.load_docs(file_path)
        docs = self.split_text(documents)

        vector_store = Chroma(
            collection_name=file_name,
            embedding_function=self.embeddings,
            persist_directory=self.db_directory
        )
        vector_store.add_documents(docs)
        vector_store.persist()
        print(f"Colección '{file_name}' creada y persistida en '{self.db_directory}'.")

    def create_collections_from_directory(self, directory_path):
        for file_name in os.listdir(directory_path):
            if file_name.endswith(".pdf"):
                file_path = os.path.join(directory_path, file_name)
                self.create_chroma_collection(file_path)


#generar_pdfs()
#cred = Credenciales()
#api_key = cred.get_huggingface_key()
#directory_path = "Informacion"  # Ruta de la carpeta con los archivos PDF
#db_directory = "./ChromaDB"  
#creacion_db = CreacionDB(api_key, db_directory=db_directory)
#creacion_db.create_collections_from_directory(directory_path)
