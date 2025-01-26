from sys import platform
from fpdf import FPDF
from langchain.agents import initialize_agent, AgentType
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.tools import Tool, tool
from conexion import ConexionDB
from modelos import Modelos 
from retriever import ConversationalRetriever
from credenciales import Credenciales
from loaddb import AbrirChromaDB
from credenciales import Credenciales
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from creardb import CreacionDB
import re
import os


@tool
def consultar_cup(especialidad):
    """ parametro: especialidad.
        proceso: Consulta el cup asociado a la especialidad suministrada.
        salida: cup.
    """
    collection_name = "Cups"  
    consulta=ConversationalRetriever(collection_name)
    chatbot = consulta.chat(especialidad)
    return chatbot


@tool
def consultar_citas_agendadas_por_paciente(documento_paciente):
    """
        Parámetro: documento del paciente (número de identificación único).
        Proceso: consulta las citas asociadas al paciente con el documento proporcionado.
        Salida: listado de las citas agendadas del paciente, incluyendo el día, el rango horario y el nombre del profesional asignado nada más, en caso de no existir citas, indicalo y termina el proceso.
    """
    collection_name = "agenda_base" 
    consulta = ConversationalRetriever(collection_name)
    chatbot = consulta.chat(f"Devuelve las citas asociadas al paciente con el documento proporcionado, en caso de no existir citas, indicalo: {documento_paciente}")
    return chatbot



@tool
def buscar_profesional_apropiado(descripcion_problema):
    """
    Parámetro: descripción_problema.
    Proceso: Analiza la descripción del problema proporcionada por el usuario para identificar qué profesional y especialidad son adecuados.
    Salida: Nombre del profesional y especialidad.
    """
    collection_name = "profesionales" 
    consulta = ConversationalRetriever(collection_name)
    chatbot = consulta.chat(descripcion_problema)  
    return chatbot


@tool
def consultar_id_profesionales_por_especialidad(especialidad):
    """
        parametro: especialidad.
        proceso: Devuelve el id del profesional asociado a esa especialidad.
        salida: id del profesional.
    """
    collection_name = "profesionales"  
    consulta=ConversationalRetriever(collection_name)

    chatbot = consulta.chat(f"Devuelve solo el identificador asociado a la especialidad: {especialidad}")
    return chatbot


@tool
def obtenercedula(input="documento del paciente"):
    """
        proceso: Obtiene el número de documento del paciente.
        salida: número de documento.
    """
    try:
        with open('cedulas_autenticadas.txt', 'r') as file:
            lineas = file.readlines()
            if lineas:
                documento = lineas[-1].strip()  
                return documento
            else:
                return "No hay cédulas registradas."
    except FileNotFoundError:
        return "Archivo no encontrado."

@tool
def consultar_id_agenda_por_horario_profesional(infoAgenda):
    """
        parametro: día de la semana junto al rango de horario y profesional id..
        proceso: Devuelve el id de la agenda asociado al día de la semana, a rango de horario y el id del profesional.
        salida: id de la agenda.
    """
    collection_name = "agenda_base"  
    consulta=ConversationalRetriever(collection_name)

    chatbot = consulta.chat(f"Devuelve el id de la agenda asociado al día de la semana, a rango de horario y el id del profesional.: {infoAgenda}")
    return chatbot

@tool
def consultar_id_disponibilidad_por_horario_profesional(infoAgenda):
    """
        parametro: día de la semana y profesional id.
        proceso: Devuelve el id de la disponibilidad y el rango de horario asociado al día de la semana e id del profesional.
        salida: id de la agdisponibilidad y rango de horarioenda.
    """
    collection_name = "disponibilidad_base"  
    consulta=ConversationalRetriever(collection_name)

    chatbot = consulta.chat(f"Devuelve el identificador asociado a la disponibilidad y el rango de horario: {infoAgenda}")
    return chatbot


@tool
def consultar_nombre_profesional_por_id(idprofesional):
    """
        parametro: id del profesional.
        proceso: Devuelve el nombre y el id del profesional asociado al id recibido.
        salida: nombre del profesional y su id.
    """
    collection_name = "profesionales"  
    consulta=ConversationalRetriever(collection_name)

    chatbot = consulta.chat(f"Devuelve el nombre y el id del profesional asociado al id: {idprofesional}")
    return chatbot

@tool
def consultar_disponibilidad_de_profesionales(id_profesionales):
    """
        parámetro: id de los profesionales o de los profesionales (puede ser un solo id o una lista).
        proceso: consulta detallada sobre cada horario de disponibilidad de los profesionales con los identificadores proporcionados.
        salida: listado con los horarios de disponibilidad de cada profesional, organizado por día y franja horaria, si no hay horarios disponibles indicalo.
    """
    collection_name = "disponibilidad_base"  

    consulta = ConversationalRetriever(collection_name)
    chatbot = consulta.chat(id_profesionales)
    
    return chatbot

@tool
def eleccion_horario_para_cita(new_row_data):
    """
    Parámetros:
        new_row_data (str): Datos del horario de la cita, incluye paciente e información del horario e id de profesional.
    Proceso:  
        agenda la cita usando el número de documento del paciente previamente dado en el chat, el dia de la cita que incluye el día y el rango de horario, 
        el id del profesional que le asignes de acuerdo a la especialidad y id del horario disponible de acuerdo al horario solicitado formato: (documento, 
        diasemana 00:00:00-00:00:00, idprofesional y el 'id' de la disponibilidad asociado a ese horario y profesional) y justo despues de terminar de agendarla, termina el proceso.
    Salida:
        str: Mensaje de éxito o error.
    """
    patron = r"(\d+),\s*([a-zA-ZáéíóúÁÉÍÓÚñÑ]+)\s*(\d{2}:\d{2}:\d{2})-(\d{2}:\d{2}:\d{2}),\s*(\d+),\s*(\d+)"
    coincidencias = re.search(patron, new_row_data)

    # Si las coincidencias son encontradas, extraemos los valores
    if coincidencias:
        paciente = coincidencias.group(1)  # Número de documento del paciente
        dia_semana = coincidencias.group(2)  # Día de la semana
        hora_inicio = coincidencias.group(3)  # Hora de inicio
        hora_fin = coincidencias.group(4)  # Hora de fin
        profesional_id = int(coincidencias.group(5))  # ID del profesional
        id = int(coincidencias.group(6))  # ID de la cita
        
        db = ConexionDB()
        if db.cursor:
            try:
              # Eliminar el horario de la tabla disponibilidad
                print(f"Ejecutando DELETE desde la tabla 'disponibilidad' con id: {id}")
                db.cursor.execute("""
                    DELETE FROM disponibilidad
                    WHERE id = %s AND profesional_id = %s AND dia_semana = %s AND hora_inicio = %s AND hora_fin = %s
                """, (id, profesional_id, dia_semana, hora_inicio, hora_fin))

                # Confirmación de eliminación
                print(f"Se envía a BD para agendar paciente: {paciente}, id: {id}, profesional_id: {profesional_id}, dia_semana: {dia_semana}, hora_inicio: {hora_inicio}, hora_fin: {hora_fin}")
                db.conn.commit()  # Guardar los cambios de eliminación
                print("DELETE ejecutado correctamente.")

                # Insertar en la tabla 'agenda'
                print("Ejecutando INSERT en la tabla 'agenda'.")
                db.cursor.execute("""
                    INSERT INTO agenda (paciente_documento, id, profesional_id, dia_semana, hora_inicio, hora_fin)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    int(paciente),                      
                    int(id),                       
                    int(profesional_id),                   
                    str(dia_semana),                    
                    str(hora_inicio),                 
                    str(hora_fin)                   
                ))

                # Confirmación de inserción
                db.conn.commit()  # Guardar los cambios de inserción
                print("INSERT ejecutado correctamente.")

                    
                db.cursor.execute("SELECT nombre FROM profesionales WHERE id = %s", (profesional_id,))
                profesional_nombre = db.cursor.fetchone()[0]

                db.cursor.execute("SELECT documento, nombre FROM paciente WHERE documento = %s", (paciente,))
                paciente_data = db.cursor.fetchone()
                
                paciente_documento = paciente_data[0]
                paciente_nombre = paciente_data[1]
                
                db.cursor.execute("SELECT especialidad FROM profesionales WHERE id = %s", (profesional_id,))
                profesional_especialidad = db.cursor.fetchone()[2]

                # Construir la información de la cita
                cita_info = {
                    "Paciente": paciente_nombre,
                    "Documento": paciente_documento,
                    "ID Cita": id,
                    "Profesional": profesional_nombre,
                    "Especialidad": profesional_especialidad,
                    "Día": dia_semana,
                    "Hora Inicio": hora_inicio,
                    "Hora Fin": hora_fin
                }

                # Generar el PDF de la cita
                generar_pdf_cita(cita_info)   
                generar_pdfs()    
                    
                try:
                    # Archivos y configuración
                    disponibilidad_path = "Informacion/disponibilidad_base.pdf"
                    agenda_path = "Informacion/agenda_base.pdf"

                    cred = Credenciales()
                    api_key = cred.get_huggingface_key()
                    abrir_db = AbrirChromaDB(api_key, db_directory="ChromaDB")
                    creacion_db = CreacionDB(api_key, db_directory="ChromaDB")

                    # Actualizar disponibilidad_base
                    disponibilidad_collection = abrir_db.load_chroma_collection("disponibilidad_base")
                    ids_to_delete = disponibilidad_collection.get()["ids"]
                    for id in ids_to_delete:
                        disponibilidad_collection.delete([id])

                    disponibilidad_docs = creacion_db.load_docs(disponibilidad_path)
                    disponibilidad_split = creacion_db.split_text(disponibilidad_docs)
                    disponibilidad_collection.add_documents(disponibilidad_split)
                    disponibilidad_collection.persist()

                    # Actualizar agenda_base
                    agenda_collection = abrir_db.load_chroma_collection("agenda_base")
                    ids_to_delete = agenda_collection.get()["ids"]
                    for id in ids_to_delete:
                         agenda_collection.delete([id])

                    agenda_docs = creacion_db.load_docs(agenda_path)
                    agenda_split = creacion_db.split_text(agenda_docs)
                    agenda_collection.add_documents(agenda_split)
                    agenda_collection.persist()
                            
                except FileNotFoundError as e:
                    return f"Error: No se encontró el archivo requerido: {e}"
                except Exception as e:
                    return f"Error inesperado: {e}"
                    
                return "El horario se ha asignado con éxito, actualizado en disponibilidad_base y registrado en agenda_base."
            except Exception as e:
                return f"Error al realizar las operaciones en la base de datos: {e}"
        else:
            return "Error al conectar a la base de datos."        
    else:
        return "Intente nuevamente. El formato de la entrada no es válido."



@tool
def cancelar_cita(texto_a_remover):
    """
    Parámetros:
        nueva_fila (str): Datos del horario de la cita, incluye paciente e información del horario, id de cita e id de profesional.
    Proceso:  
        cancela la cita usando el número de documento del paciente previamente dado en el chat, el dia de la cita que incluye el día y el rango de horario, el id del profesional que le asignes de acuerdo a la especialidad y el id de la agenda de acuerdo al horario y profesional. formato: (documento, diasemana 00:00:00-00:00:00, idprofesional, idagenda (tomado de agenda_base)).
    Salida:
        str: Mensaje de éxito o error.
    """
    patron = r"^(\d+),\s*([a-zA-ZáéíóúÁÉÍÓÚñÑ]+)\s*(\d{2}:\d{2}:\d{2})-(\d{2}:\d{2}:\d{2}),\s*(\d+),\s*(\d+)$"
    coincidencias = re.match(patron, texto_a_remover)
    
    if coincidencias:
        paciente = coincidencias.group(1)
        dia_semana = coincidencias.group(2)
        hora_inicio = coincidencias.group(3)
        hora_fin = coincidencias.group(4)
        profesional_id = int(coincidencias.group(5))
        id_cita = int(coincidencias.group(6))
        db = ConexionDB()
        if db.cursor:
            try:
                print("Ejecutando DELETE desde la tabla 'agenda' con id:", id_cita)
                db.cursor.execute("""
                    DELETE FROM agenda
                    WHERE id = %s AND  profesional_id = %s AND paciente_documento = %s AND dia_semana = %s AND hora_inicio = %s AND hora_fin = %s
                """, (id_cita, profesional_id, paciente, dia_semana, hora_inicio, hora_fin))

                # Confirmación de eliminación
                print(f"Se envía a BD para cancelar: paciente: {paciente}, id: {id_cita}, profesional_id: {profesional_id}, dia_semana: {dia_semana}, hora_inicio: {hora_inicio}, hora_fin: {hora_fin}")
                db.conn.commit()  # Guardar los cambios de eliminación
                print("DELETE ejecutado correctamente.")

                print("Ejecutando INSERT en la tabla 'disponibilidad'.")
                db.cursor.execute("""
                    INSERT INTO disponibilidad (id, profesional_id, dia_semana, hora_inicio, hora_fin)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    id_cita,                       
                    profesional_id,                       
                    dia_semana,                          
                    hora_inicio,                       
                    hora_fin                         
                ))

                # Confirmación de inserción
                db.conn.commit()  # Guardar los cambios de inserción
                print("INSERT ejecutado correctamente.")

                generar_pdfs()
                
                try:
                    # Ahora procedemos con el resto del proceso
                    pdf_path = "Informacion/agenda_base.pdf"
                    disponibilidad_path = "Informacion/disponibilidad_base.pdf"
                    
                    # Actualización de las colecciones en ChromaDB
                    cred = Credenciales()
                    api_key = cred.get_huggingface_key() 
                    abrir_db = AbrirChromaDB(api_key, db_directory="ChromaDB")
                    creacion_db = CreacionDB(api_key, db_directory="ChromaDB")

                    # Actualizar agenda_base
                    agenda_collection = abrir_db.load_chroma_collection("agenda_base")
                    agenda_ids_to_delete = agenda_collection.get()["ids"]
                    for id in agenda_ids_to_delete:
                        agenda_collection.delete([id])

                    agenda_docs = creacion_db.load_docs(pdf_path)
                    agenda_split = creacion_db.split_text(agenda_docs)
                    agenda_collection.add_documents(agenda_split)
                    agenda_collection.persist()

                    # Actualizar disponibilidad_base
                    disponibilidad_collection = abrir_db.load_chroma_collection("disponibilidad_base")
                    disponibilidad_ids_to_delete = disponibilidad_collection.get()["ids"]
                    for id in disponibilidad_ids_to_delete:
                        disponibilidad_collection.delete([id])

                    disponibilidad_docs = creacion_db.load_docs(disponibilidad_path)
                    disponibilidad_split = creacion_db.split_text(disponibilidad_docs)
                    disponibilidad_collection.add_documents(disponibilidad_split)
                    disponibilidad_collection.persist()
                except FileNotFoundError:
                    return f"Error: El archivo original '{pdf_path}' no existe."
                except Exception as e:
                    return f"Error inesperado: {e}"

                return "Cita cancelada con éxito, actualizado en disponibilidad_base y registrado en agenda_base."
            except Exception as e:
                print(f"Error al realizar las operaciones en la base de datos: {e}")
                return f"Error al realizar las operaciones en la base de datos: {e}"
        else:
            return "Error al conectar a la BD."
    else:
        return "Intente nuevamente. El formato de la entrada no es válido."


def generar_pdf_cita(cita):
    """
    Proceso: Genera un PDF con la información de la cita asignada, utilizando un formato hospitalario profesional.
    Parámetros:
        cita (dict): Información de la cita con las claves:
            - Paciente: Nombre del paciente.
            - Documento: Documento del paciente.
            - ID Cita: Identificador único de la cita.
            - Profesional: Nombre del profesional.
            - Especialidad: Especialidad del profesional.
            - Día: Día de la cita.
            - Hora Inicio: Hora de inicio de la cita.
            - Hora Fin: Hora de finalización de la cita.
    Salida:
        str: Ruta del archivo PDF generado.
    """
    
    # Ruta de salida del PDF
    pdf_path = os.path.join(os.getcwd(), "cita_asignada.pdf")
    
    # Crear el objeto canvas para generar el PDF
    c = canvas.Canvas(pdf_path, pagesize=letter)
    
    # Configuración de estilo
    c.setFont("Helvetica", 12)
    
    # Información de la cabecera
    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, 750, "HOSPITAL UNIVERSITARIO SAN JOSÉ")
    c.setFont("Helvetica", 10)
    c.drawString(30, 735, "Dirección: Calle 45 #123-45, Bogotá, Colombia")
    c.drawString(30, 720, "Teléfono: (601) 555-6789")
    
    # Título de la sección
    c.setFont("Helvetica-Bold", 16)
    c.drawString(250, 680, "Autorización cita")
    
    # Información de la cita (en una tabla simple)
    c.setFont("Helvetica", 12)
    c.drawString(30, 650, f"Paciente: {cita.get('Paciente', 'N/A')}")
    c.drawString(30, 635, f"Documento: {cita.get('Documento', 'N/A')}")
    c.drawString(30, 620, f"ID de la Cita: {cita.get('ID Cita', 'N/A')}")
    c.drawString(30, 605, f"Profesional: {cita.get('Profesional', 'N/A')}")
    c.drawString(30, 590, f"Especialidad: {cita.get('Especialidad', 'N/A')}")
    c.drawString(30, 575, f"Día: {cita.get('Día', 'N/A')}")
    c.drawString(30, 560, f"Hora de Inicio: {cita.get('Hora Inicio', 'N/A')}")
    c.drawString(30, 545, f"Hora de Fin: {cita.get('Hora Fin', 'N/A')}")
    
    # Pie de página
    c.setFont("Helvetica", 10)
    c.drawString(30, 500, "Presentarse 40 minutos antes de la cita.")
    c.drawString(30, 485, "Para cambios o cancelaciones, use el asistente inteligente.")
    
    # Nota
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(30, 450, "Este documento es una confirmación oficial de su cita médica. Si tiene alguna duda, por favor contáctenos.")
    
    # Guardar el PDF
    c.save()

    return pdf_path



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

    finally:
        conexion.cerrar_conexion()




class AgenteSolicitanteDatos:
    def __init__(self):
        modelo = Modelos()
        self.llm = modelo.get_llm()

        self.tools = [
            Tool(name="consultar_cup", func=consultar_cup, description="Consulta el cup asociado a la especialidad suministrada"),
            Tool(name="consultar_id_profesionales_por_especialidad", func=consultar_id_profesionales_por_especialidad,description="Devuelve el id del profesional asociado a esa especialidad"),
            Tool(name="consultar_disponibilidad_de_profesionales", func=consultar_disponibilidad_de_profesionales,description="Consulta cada horario de disponibilidad de los id de los profesionales"),
            Tool(name="eleccion_horario_para_cita", func=eleccion_horario_para_cita,description="agenda la cita usando el número de documento del paciente previamente dado en el chat, el dia de la cita que incluye el día y el rango de horario, el id del profesional que le asignes de acuerdo a la especialidad y id del horario disponible de acuerdo al horario solicitado formato: (documento, diasemana 00:00:00-00:00:00, idprofesional y el 'id' de la disponibilidad asociado a ese horario y profesional) y justo despues de terminar de agendarla, termina el proceso."),
            Tool(name="consultar_id_agenda_por_horario_profesional", func=consultar_id_agenda_por_horario_profesional,description="Devuelve el id de la agenda asociado al día de la semana, a rango de horario y el id del profesional."),
            Tool(name="cancelar_cita", func=cancelar_cita,description="cancela la cita usando el número de documento del paciente previamente dado en el chat, el dia de la cita que incluye el día y el rango de horario, el id del profesional que le asignes de acuerdo a la especialidad y el id de la agenda de acuerdo al horario y profesional. formato: (documento, diasemana 00:00:00-00:00:00, idprofesional, idagenda (tomado de agenda_base))."),
            Tool(name="consultar_citas_agendadas_por_paciente", func=consultar_citas_agendadas_por_paciente,description="consulta las citas asociadas al paciente con el documento proporcionado."),
            Tool(name="consultar_nombre_profesional_por_id", func=consultar_nombre_profesional_por_id,description="Devuelve el nombre y el id del profesional asociado al id recibido."),
            Tool(name="consultar_id_disponibilidad_por_horario_profesional", func=consultar_id_disponibilidad_por_horario_profesional,description="Devuelve el id de la disponibilidad y el rango de horario asociado al día de la semana e id del profesional."),
            Tool(name="obtenercedula", func=obtenercedula,description="Obtiene el número de documento del paciente."),
            Tool(name="buscar_profesional_apropiado", func=buscar_profesional_apropiado,description="Analiza la descripción del problema proporcionada por el usuario para identificar qué profesional y especialidad son adecuados.")  
        ]

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "Eres un asistente para consultar y suministrar información del proceso para agendar citas"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        self.memory = ConversationBufferMemory(memory_key="chat_history", input_key="input")

        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            prompt=self.prompt,
            memory=self.memory,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            iteration_limit=10,
            return_intermediate_steps=False,
            handle_parsing_errors=True,
        )

    def chat(self, input):
        try:
            response = self.agent.invoke({'input': input})
            if isinstance(response, dict):
                response_text = response.get("content", "")
            else:
                response_text = str(response)

            self.memory.save_context(
                {"input": input},       
                {"output": response_text}    
            )
            return response
        except Exception as e:
            return str(e)


if __name__ == "__main__":
    agente = AgenteSolicitanteDatos()
