import os
from fastapi import FastAPI, Request, File, UploadFile
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.traductor import traductor_func
from app.video import video_func
from app.scanTexto import scanTexto_func


origins = ["*"]

app = FastAPI()

class Libro(BaseModel):
    titulo: str
    autor: str
    paginas: int
    editorial: str
    
class ScanTexto(BaseModel):
    image_path: str
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/")
def index():
    return {"message" : "Hola, Pythonianos"}

@app.get("/libros/({id}")
def mostrar_libro(id: int):
    return {"data": id}

@app.get("/libros")
def mostrar_libros():
    return {"data": "Lista de libros"}

@app.post("/libros")
def insertar_libro(libro: Libro):
    return {"message": f"libro (libro.titulo) insertado"}

@app.put("/libros/{id}")
def actualizar_libro(id: int, libro: Libro):
    return {"message": f"libro (libro.titulo) actualizado"}

@app.delete("/libros/{id}")
def eliminar_libro(id: int):
    return {"message": f"libro (libro.titulo) eliminado"}


@app.post("/uploadfile/")
async def create_upload_file(imagePath: UploadFile):
    """
    Sube un archivo de imagen y lo guarda en el servidor.

    Argumentos:
        imagePath (UploadFile): El archivo de imagen cargado por el usuario.

    Retorno:
        str: El nombre del archivo guardado y su ruta completa.
    """
    filename = imagePath.filename
    contents = await imagePath.read()

    # Guardar el archivo en el servidor
    with open(f"uploads/{filename}", "wb") as file:
        file.write(contents)

    saved_file_path = os.path.join(f"uploads/{filename}")
    return {"filename": filename, "saved_file_path": saved_file_path}


@app.post("/process_image")
async def process_image_endpoint(image: UploadFile = File(...),
    task: str = "original",
        **kwargs):
    """
    API endpoint for processing images using OpenCV.

    Args:
        image (UploadFile): The image file uploaded by the user.
        task (str, optional): The image processing task to perform.
            Defaults to "original" (returns the original image).
        **kwargs: Additional keyword arguments specific to each task.

    Returns:
        bytes: The processed image data.
    """
    processed_image = await UploadFile(image, task, **kwargs)
    return processed_image


    
@app.post("/scanTexto")
async def scanTexto_endpoint(request: Request, scanTexto_data: ScanTexto):
    image_path = scanTexto_data.image_path

    try:
        escaner = scanTexto_func(image_path)
        return {"data": escaner}
    except Exception as e:
        print(f"Error extracting text: {e}")
        return {"error": str(e)}


class TraductorRequest(BaseModel):
    translate_text: str
    target_lang: str

@app.get("/video")
def video():
    return video_func()

@app.post("/traductor")
async def traductor_endpoint(request: Request, traductor_data: TraductorRequest):
    translate_text = traductor_data.translate_text
    target_lang = traductor_data.target_lang
    traduccion = traductor_func(translate_text, target_lang)
    return {"data": traduccion}

