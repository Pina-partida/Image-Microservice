from fastapi import FastAPI, UploadFile, File, HTTPException
from PIL import Image
import os
import io

app = FastAPI()
ALLOWED = {"png", "jpg", "jpeg"}

def image_channel(source_folder: str, destination_folder: str, file: UploadFile, image_type: str = "original"):
    try:
        # this is for setup of source and destinTION
        os.makedirs(source_folder, exist_ok=True) #access and define source_folder this is why we import os, 2nd arg is for logic
        os.makedirs(destination_folder, exist_ok=True) #access and define source_folder this is why we import os
        
        # Check file.filename not path.filename to verify extension
        file_type = file.filename.split(".")[-1].lower()
        if file_type not in ALLOWED:
            return (False, "Unsupported file type") #boolean needed for Exception


        # Save original preserve file_type with fole_type
        image_bytes = file.file.read() # has to be
        image_file_path = os.path.join(source_folder, f"{image_name}{file_type}")
        image.save(image_file_path, {file_type})


        image = Image.open(io.BytesIO(image_bytes)).convert("RGBA")  # io is needed
        image_name = os.path.splitext(file.filename)[0]


        # Check logic based on img_type argument
        if image_type == "original": # jpeg, jpg, png converts to png
            pass

        elif image_type == "thumbnail":

            pass

@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):

    success, message = image_channel(
        source_folder="uploads",
        destination_folder="thumbnails",
        file=file
    )

    if not success:
        raise HTTPException(status_code=400, detail="Upload unsuccesful")
