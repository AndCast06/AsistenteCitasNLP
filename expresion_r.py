import re
from datetime import datetime, timedelta
from fpdf import FPDF
import PyPDF2

def generar_intervalos(hora_inicio, hora_fin):
    inicio = datetime.strptime(hora_inicio, '%H:%M:%S')
    fin = datetime.strptime(hora_fin, '%H:%M:%S')
    intervalos = []
    while inicio < fin:
        siguiente = inicio + timedelta(minutes=30)
        intervalos.append((inicio.strftime('%H:%M:%S'), siguiente.strftime('%H:%M:%S')))
        inicio = siguiente
    return intervalos

def leer_pdf(ruta_pdf):
    with open(ruta_pdf, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        texto = ""
        for pagina in reader.pages:
            texto += pagina.extract_text()
    return texto

patron = r"id:\s*(\d+),\s*profesional_id:\s*(\d+),\s*dia_semana:\s*(\w+),\s*hora_inicio:\s*([\d:]+),\s*hora_fin:\s*([\d:]+)"

ruta_pdf_entrada = "Informacion/disponibilidad.pdf"
contenido = leer_pdf(ruta_pdf_entrada)

pdf = FPDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=10)
pdf.set_font("Arial", size=12)

for coincidencia in re.finditer(patron, contenido):
    id_, profesional_id, dia_semana, hora_inicio, hora_fin = coincidencia.groups()
    intervalos = generar_intervalos(hora_inicio, hora_fin)
    for inicio, fin in intervalos:
        pdf.cell(0, 10, f"id: {id_}, profesional_id: {profesional_id}, dia_semana: {dia_semana}, hora_inicio: {inicio}, hora_fin: {fin}.", ln=True)

pdf.output("Informacion/disponibilidad_base.pdf")
