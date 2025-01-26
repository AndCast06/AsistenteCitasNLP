import fitz  # PyMuPDF
import re
import os

def process_pdf(texto_a_remover):
    """
    Parámetros:
        texto_a_remover (str): Texto que se desea eliminar del PDF.
    Proceso:
        Crea un nuevo archivo PDF con el texto removido, centrando el contenido y eliminando espacios en blanco.
    Salida:
        str: Mensaje de éxito o error.
    """
    pdf_path = "agenda/disponibilidad_base.pdf"
    output_pdf_path = "agenda/disponibilidad_base_nuevo.pdf"
    
    escaped_text = re.escape(texto_a_remover)
    pattern = rf"{escaped_text}"

    try:
        doc = fitz.open(pdf_path)
        new_doc = fitz.open()

        for page_num, page in enumerate(doc, start=1):
            text = page.get_text("text") 
            if text:
                updated_lines = [
                    line for line in text.splitlines() if not re.search(pattern, line)
                ]
                updated_text = "\n".join(updated_lines)

                new_page = new_doc.new_page(width=page.rect.width, height=page.rect.height)

                font_size = 10
                margin = 72 
                y_offset = margin  

                for line in updated_lines:
                    new_page.insert_text(
                        (margin, y_offset), line, fontsize=font_size
                    )
                    y_offset += font_size + 2  

        new_doc.save(output_pdf_path)
        new_doc.close()
        doc.close()

        if os.path.exists(pdf_path):
            os.remove(pdf_path)

        os.rename(output_pdf_path, pdf_path)

        return f"El archivo PDF ha sido actualizado exitosamente y el archivo original ha sido reemplazado."
    
    except FileNotFoundError:
        return f"Error: El archivo original '{pdf_path}' no existe."
    except Exception as e:
        return f"Error inesperado: {e}"

# Texto a eliminar del PDF
text_to_remove = "id: 6, profesional_id: 6, dia_semana: Lunes, hora_inicio: 08:00:00, hora_fin: 08:30:00"
result = process_pdf(text_to_remove)
print(result)
