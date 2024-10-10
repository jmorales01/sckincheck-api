from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Text, Optional
from datetime import datetime
import base64
import os
from fastapi.middleware.cors import CORSMiddleware
from procesar import ejecutar_script_deteccion
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/assets", StaticFiles(directory="assets"), name="assets")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TEMP_IMAGE_DIR = './tmp'

# Model
class ImageUpload(BaseModel):
    user: str
    image_base64: str 
    description: Optional[str]

@app.get('/')
def read_root():
    return {"api": "Hello word"}


@app.post('/upload_image')
def upload_image(image_data: ImageUpload):
    try:
        image_bytes = base64.b64decode(image_data.image_base64)
        image_filename = f"{image_data.user or 'image'}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        image_path = os.path.join(TEMP_IMAGE_DIR, image_filename)

        # Asegurarse de que el directorio temporal exista y guardar
        os.makedirs(TEMP_IMAGE_DIR, exist_ok=True)
        with open(image_path, "wb") as image_file:
            image_file.write(image_bytes)

        # Pasar la imagen a la función de análisis
        return_path, result = ejecutar_script_deteccion(image_path,image_data.user)

        return {
            'message': 'Image processed successfully',
            'url_image': return_path,
            'result': result
        }
    except base64.binascii.Error as e:
        raise HTTPException(status_code=400, detail="Invalid base64 string")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
