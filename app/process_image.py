from app.scanTexto import UploadFile
from fastapi import UploadFile
import cv2
import numpy as np

async def process_image(imagePath: UploadFile, task: str, **kwargs):
    """
    Procesos una imagen cargada usando OpenCV.

    Args:
        imagePath (UploadFile): El archivo de imagen cargado por el usuario.
        task (str): La tarea de procesamiento de imagen a realizar.
        **kwargs: Argumentos de palabra clave adicionales específicos de cada tarea.
    Retorno:
        bytes: Los datos de la imagen procesada.
    """
    # Leer la imagen
    img = cv2.imdecode(np.fromstring(await imagePath.read(), np.uint8), cv2.IMREAD_COLOR)

    #
