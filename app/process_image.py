from fastapi import FastAPI, File, UploadFile
import cv2
import numpy as np
import asyncio
from typing import Optional

async def process_image(image: UploadFile, task: str, **kwargs):
    """
    Processes an uploaded image using OpenCV.
    Args:
        image (UploadFile): The image file uploaded by the user.
        task (str): The image processing task to perform.
        **kwargs: Additional keyword arguments specific to each task.
    Returns:
        bytes: The processed image data.
    """
    # Read the image
    img = cv2.imdecode(np.fromstring(await image.read(), np.uint8), cv2.IMREAD_COLOR)
    
    # Handle different processing tasks with specific parameters
    processed_img = None
    if task == "draw_rectangle":
        # ... (code for drawing rectangle with default and optional parameters)
        pass
    elif task == "grayscale":
        # ... (code for converting to grayscale)
        pass
    elif task == "resize":
        # ... (code for resizing with default and optional parameters)
        pass
    # ... (similar logic for other tasks)
    else:
        return {"error": "Invalid task. Supported tasks: draw_rectangle, grayscale, resize, rotate, crop, blur, sharpen, canny_edges"}
    
    # Encode and return the processed image
    ret, buffer = cv2.imencode('.jpg', processed_img)
    return buffer.tobytes()