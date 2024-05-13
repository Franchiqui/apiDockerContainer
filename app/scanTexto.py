from fileinput import filename
from app.process_image import UploadFile
import numpy as np
import cv2
import pytesseract

def scanTexto_func(imagePath: str, task="original", **kwargs):

    """
    Extrae texto de una imagen y lo devuelve como cadena.

    Argumentos:
        imagePath (str): Ruta al archivo de imagen a escanear.

    Retorno:
        str: El texto extraído de la imagen.
    """

    # Cargar la imagen
    img = cv2.imread(imagePath)

    # Compruebe si la imagen se leyó correctamente.
    if img is None:
        raise Exception("Error loading image: {}".format(imagePath))

    # Aplicar el preprocesamiento de la imagen según la tarea
    if task == "original":
        processed_img = img
    elif task == "grayscale":
        processed_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        # ... (Implementar preprocesamiento para otras tareas)
        pass
    
    # Establecer la ruta de Tesseract
    pytesseract.pytesseract.tesseract_cmd = r'C:/Archivos de programa/Tesseract-OCR/tesseract.exe'

    # Establecer el idioma del texto
    text = pytesseract.image_to_string(processed_img, config='--psm 10 lang=es')

    # Devolver el texto extraído
    return text



