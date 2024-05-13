from fastapi import FastAPI, File, UploadFile
import cv2
import numpy as np

app = FastAPI()

@app.post("/process_image")
async def process_image(image: UploadFile = File(...),
                        task: str = "original",  # Default task
                         **kwargs):  # Capture additional parameters for flexibility
    """
    Punto final API para procesar imágenes usando OpenCV.

    Args:
        image (UploadFile): El archivo de imagen subido por el usuario.
        task (str, optional): La tarea de procesamiento de imágenes a realizar.
            El valor predeterminado es "original" (devuelve la imagen original).
        **kwargs: Additional keyword arguments specific to each task.

    Returns:
        bytes: Los datos de la imagen procesada.
    """

    # Lee la imagen
    img = cv2.imdecode(np.fromstring(await UploadFile.read(), np.uint8), cv2.IMREAD_COLOR)

    # Manejar diferentes tareas de procesamiento con parámetros específicos
    processed_img = None
    if task == "draw_rectangle":
        x1, y1, x2, y2 = kwargs.get("coordinates", (0, 0, img.shape[1], img.shape[0]))  # Imagen completa predeterminada
        color = kwargs.get("color", (0, 255, 0))  # Verde predeterminado
        thickness = kwargs.get("thickness", 2)
        processed_img = cv2.rectangle(img.copy(), (x1, y1), (x2, y2), color, thickness)
    elif task == "grayscale":
        processed_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif task == "resize":
        width, height = kwargs.get("size", (img.shape[1], img.shape[0]))  # Tamaño original predeterminado
        processed_img = cv2.resize(img, (width, height))
    elif task == "rotate":
        angle = kwargs.get("angle", 0)  # Rotación predeterminada de 0 grados
        center = (img.shape[1] // 2, img.shape[0] // 2)
        scale = kwargs.get("scale", 1.0)  # Factor de escala predeterminado
        M = cv2.getRotationMatrix2D(center, angle, scale)
        processed_img = cv2.warpAffine(img, M, (img.shape[1], img.shape[0]))
    elif task == "crop":
        top, left, bottom, right = kwargs.get("bounding_box", (0, 0, img.shape[0], img.shape[1]))  # Default entire image
        processed_img = img[UploadFile]
    elif task == "blur":
        kernel_size = kwargs.get("kernel_size", (5, 5))  # Núcleo 5x5 predeterminado
        processed_img = cv2.blur(img, kernel_size)
    elif task == "sharpen":
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        processed_img = cv2.filter2D(img.copy(), -1, kernel)
    elif task == "canny_edges":
        threshold1, threshold2 = kwargs.get("thresholds", (100, 200))  # Umbrales de detección de bordes Canny predeterminados
        processed_img = cv2.Canny(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), threshold1, threshold2)
    else:
        return {"error": "Tarea no válida. Tareas admitidas: draw_rectangle, grayscale, resize, rotate, crop, blur, sharpen, canny_edges"}

    # Codificar y devolver la imagen procesada.
    ret, buffer = cv2.imencode('.jpg', processed_img)
    return buffer.tobytes()
