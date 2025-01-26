import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableSequence, RunnablePassthrough
from conexion import ConexionDB  # Importa la clase de conexión a la base de datos
from agente import AgenteSolicitanteDatos  # Importa la clase del agente


class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Asistente de Agendamiento de Citas Médicas")
        self.setGeometry(100, 100, 600, 600)

        # Inicialización de variables
        self.agente = None
        self.cedula = None
        self.password = None
        self.datos_recopilados = False
        self.db = ConexionDB()

        # Interfaz de usuario
        main_layout = QVBoxLayout()

        # Encabezado
        header = QLabel("💬 Asistente de Agendamiento")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("""
            font-size: 18pt; 
            font-weight: bold; 
            background-color: #ad3333; 
            color: white; 
            padding: 10px;
        """)
        main_layout.addWidget(header)

        # Área de texto para mostrar el chat
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setStyleSheet("""
            background-color: #f9f9f9; 
            font-size: 12pt; 
            padding: 10px; 
            border: none;
        """)
        main_layout.addWidget(self.chat_area)

        # Campo de entrada y botón de envío
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Escribe tu mensaje aquí...")
        self.input_field.setStyleSheet("""
            padding: 10px; 
            font-size: 11pt; 
            border: 2px solid #ad3333; 
            border-radius: 10px;
        """)
        self.input_field.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_field)

        self.send_button = QPushButton("Enviar")
        self.send_button.setStyleSheet("""
            background-color: #ad3333;
            color: white;
            font-size: 11pt;
            padding: 8px 16px;
            border-radius: 10px;
            border: none;
        """)
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)

        main_layout.addLayout(input_layout)

        # Contenedor
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Inicio del flujo
        self.display_message("Por favor, ingresa tu número de cédula:", "assistant")

    def autenticar_usuario(self, cedula):
        """Valida la cédula del usuario contra la base de datos"""
        query = "SELECT nombre FROM paciente WHERE documento = %s"
        result = self.db.ejecutar_query(query, (cedula,), fetch_one=True)
        return result

    def validar_contraseña(self, cedula, password):
        """Valida la contraseña del usuario asociado a la cédula"""
        query = "SELECT password FROM paciente WHERE documento = %s"
        result = self.db.ejecutar_query(query, (cedula,), fetch_one=True)
        if result:
            return result[0] == password  # Comparar directamente si no hay hashing
        return False

    def send_message(self):
        user_message = self.input_field.text().strip()

        if user_message:
            self.display_message(user_message, "user")
            self.input_field.clear()

            try:
                if not self.datos_recopilados:
                    # Paso 1: Validar cédula
                    if self.cedula is None:
                        self.cedula = user_message
                        usuario = self.autenticar_usuario(self.cedula)
                        if usuario:
                            self.display_message(f"Usuario encontrado: {usuario[0]}. Por favor, ingresa tu contraseña:", "assistant")
                            self.input_field.setEchoMode(QLineEdit.Password)  # Activar modo de contraseña
                        else:
                            self.display_message("Cédula no encontrada. Por favor, acérquese a su centro de salud para registrarse.", "assistant")
                            self.cedula = None  # Restablecer para permitir otro intento

                    # Paso 2: Validar contraseña
                    elif self.password is None:
                        self.password = user_message
                        if self.validar_contraseña(self.cedula, self.password):
                            self.display_message("¡Autenticación exitosa! ¿En qué puedo ayudarte?", "assistant")
                            self.datos_recopilados = True

                            # Inicializar agente y guardar cédula
                            self.agente = AgenteSolicitanteDatos()
                            with open('cedulas_autenticadas.txt', 'a') as file:
                                file.write(self.cedula + '\n')

                            self.input_field.setEchoMode(QLineEdit.Normal)  # Desactivar modo de contraseña
                        else:
                            self.display_message("Contraseña incorrecta. Intente nuevamente:", "assistant")
                            self.password = None  # Restablecer para permitir reintento
                    else:
                        self.display_message("Por favor, completa el paso anterior.", "assistant")

                else:
                    # Flujo normal del agente
                    assistant_response = self.agente.chat(user_message)
                    if isinstance(assistant_response, dict) and 'output' in assistant_response:
                        assistant_response = assistant_response['output']
                    elif isinstance(assistant_response, str):
                        pass
                    else:
                        assistant_response = "No se pudo obtener una respuesta válida."

                    self.display_message(assistant_response, "assistant")

            except Exception as e:
                self.display_message(f"Error al procesar la solicitud: {e}", "assistant")

    def display_message(self, message, sender):
        if sender == "user":
            formatted_message = f'''
                <div style="display: flex; align-items: center; justify-content: flex-end; margin: 10px;">
                    <span style="
                        background-color: #f1f1f1; 
                        color: #333; 
                        padding: 10px; 
                        border-radius: 10px; 
                        max-width: 60%; 
                        box-shadow: 0px 3px 6px rgba(0, 0, 0, 0.1); 
                        font-size: 11pt; 
                        word-wrap: break-word; 
                        text-align: left;">
                        <b>👤 User: </b>{message}
                    </span>
                </div>
            '''
        else:
            llm = ChatOpenAI(temperature=0, model="gpt-4o-mini", api_key= "")
            prompt_template = f"""
            el texto es lo siguiente:
            {message}
            Detecta si el texto viene en español o en inglés, en caso de que sea inglés traduce a Español de forma correcta.
            No añadas nada más que no sea la traducción al Español del texto.
            """
            prompt = PromptTemplate(
                input = message, 
                template=prompt_template
            )
            output_parser = StrOutputParser()
            llm_chain = RunnableSequence(
                {
                    "message": RunnablePassthrough()
                }
                | prompt
                | llm
                | output_parser
            )
            result = llm_chain.invoke(message)

            formatted_message = f'''
                <div style="display: flex; align-items: center; margin: 10px;">           
                    <span style="
                        background-color: #f1f1f1; 
                        color: #333; 
                        padding: 10px; 
                        border-radius: 10px; 
                        max-width: 60%; 
                        box-shadow: 0px 3px 6px rgba(0, 0, 0, 0.1); 
                        font-size: 11pt; 
                        word-wrap: break-word; 
                        text-align: left;">
                        <b>🤖 Asistente: </b>{result}
                    </span>
                </div>
            '''
        self.chat_area.append(formatted_message)
        self.chat_area.moveCursor(QTextCursor.End)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec_())
