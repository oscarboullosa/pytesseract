import pytesseract
from PIL import Image
import sys
import io
from logger import log_ocr_error, print_error
from notifications import notify
from PyQt5 import QtCore
from messages import ocr_error_message

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

def ensure_tesseract_installed():
    try:
        pytesseract.get_tesseract_version()
    except EnvironmentError:
        notify(
            "Tesseract is either not installed or cannot be reached.\n"
            "Have you installed it and added the install directory to your system path?"
        )
        print_error(
            "Tesseract is either not installed or cannot be reached.\n"
            "Have you installed it and added the install directory to your system path?"
        )
        sys.exit()


def get_ocr_result(img, lang=None):
    buffer = QtCore.QBuffer()
    buffer.open(QtCore.QBuffer.ReadWrite)
    img.save(buffer, "PNG")
    pil_img = Image.open(io.BytesIO(buffer.data()))
    buffer.close()

    try:
        return pytesseract.image_to_string(pil_img, timeout=5, lang=lang).strip()
    except RuntimeError as error:
        log_ocr_error(error)
        notify(ocr_error_message(error))
        return

"""
Se crea un objeto QBuffer de Qt para almacenar datos en memoria.
La imagen img se guarda en este búfer en formato PNG.

Se crea una imagen de tipo Image utilizando la biblioteca PIL a partir de los datos almacenados en el búfer.

Se utiliza la biblioteca pytesseract para realizar OCR en la imagen convertida.
pytesseract.image_to_string toma la imagen PIL (pil_img) y devuelve el texto extraído de la imagen.
Se ha especificado un tiempo de espera (timeout=5) para evitar bloqueos prolongados en caso de problemas.
Si se produce un error durante el proceso OCR, se captura la excepción RuntimeError.
Se llama a las funciones log_ocr_error y notify para registrar el error y notificarlo de alguna manera.
Si ocurre un error, la función devuelve None.

Esta función toma una imagen como entrada, realiza OCR en ella utilizando Tesseract a través de la biblioteca pytesseract, y devuelve el texto extraído. Si se encuentra algún error durante el proceso, se registra y notifica, y la función devuelve None.
"""