import os
import fitz  # Para manejo de PDFs
from docx2pdf import convert  # Para convertir .docx a PDF
import win32com.client as win32  # Para convertir .doc a .docx

# Ruta de carpeta
DIR = r"C:\Users\eechever\Desktop\verificar"

def doc_to_docx(ruta_doc):
    """Convierte .doc a .docx."""
    try:
        word = win32.Dispatch("Word.Application")
        doc = word.Documents.Open(ruta_doc)
        docx_path = ruta_doc.replace(".doc", ".docx")
        doc.SaveAs2(docx_path, FileFormat=16)
        doc.Close()
        word.Quit()
        return docx_path
    except Exception as e:
        print(f"Error al convertir {ruta_doc}: {e}")
        return None

def to_pdf(ruta_docx):
    """Convierte .docx a PDF."""
    try:
        pdf_path = ruta_docx.replace(".docx", ".pdf")
        convert(ruta_docx, pdf_path)
        return pdf_path
    except Exception as e:
        print(f"Error al convertir {ruta_docx} a PDF: {e}")
        return None

def paginas_blancas(pdf_path):
    """Verifica páginas en blanco en PDF."""
    try:
        with fitz.open(pdf_path) as doc:
            return [i + 1 for i, pag in enumerate(doc) if not pag.get_text().strip()]
    except Exception as e:
        print(f"Error leyendo {pdf_path}: {e}")
        return []

def procesar_archivos(carpeta, procesar_subcarpetas=False):
    """Procesa todos los archivos .doc y .docx en la carpeta y subcarpetas (opcional)."""
    archivos_procesados = []
    archivos_creados = []

    for raiz, dirs, archivos in os.walk(carpeta):
        # Si no se deben procesar subcarpetas, vacía `dirs` para evitar que se recorran
        if not procesar_subcarpetas:
            dirs[:] = []

        for archivo in archivos:
            if archivo.endswith((".docx", ".doc")):
                ruta = os.path.join(raiz, archivo)

                # Convertir .doc a .docx si es necesario
                if archivo.endswith(".doc"):
                    ruta = doc_to_docx(ruta)
                    if not ruta: continue

                # Convertir .docx a PDF
                pdf_path = to_pdf(ruta)
                if pdf_path:
                    archivos_creados.append(pdf_path)

                    # Verificar páginas en blanco
                    blancas = paginas_blancas(pdf_path)

                    # Obtener la ruta relativa del archivo desde la carpeta base
                    ruta_relativa = os.path.relpath(raiz, carpeta)

                    # Almacenar la información del archivo junto con la subcarpeta
                    archivos_procesados.append({
                        'nombre': archivo,
                        'ruta': ruta_relativa,
                        'blancas': blancas
                    })

                    # Mostrar el resultado, incluyendo la ruta
                    if blancas:
                        print(f"{archivo} en la subcarpeta '{ruta_relativa}' tiene páginas en blanco: {blancas}")
                    else:
                        print(f"{archivo} en la subcarpeta '{ruta_relativa}' no tiene páginas en blanco.")

    # Eliminar archivos creados
    for archivo in archivos_creados:
        try:
            os.remove(archivo)
            print(f"Archivo eliminado: {archivo}")
        except Exception as e:
            print(f"Error al eliminar {archivo}: {e}")

    # Resumen final
    print("\nProceso completado.")
    return archivos_procesados

if __name__ == "__main__":
    procesar_subcarpetas = input("¿Desea procesar las subcarpetas? (s/N): ").lower() in ["s", "y"]
    procesar_archivos(DIR, procesar_subcarpetas)
