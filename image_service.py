from fastapi import FastAPI, UploadFile, File, HTTPException
from PIL import Image
import os
import io
# dont use pathlib from Path because user willl define directories

app = FastAPI()
ALLOWED = {"png", "jpg", "jpeg", "bmp", "gif", "tiff", "webp"}

def image_channel(source_folder: str, destination_folder: str, file: UploadFile, action: str = "original"):
    
    try:
        
        # this is for setup of source and destinTION, makesdirs() normally makes a diectory but we're using it for comfirmation
        os.makedirs(source_folder, exist_ok=True) #access and define source_folder this is why we import os, 2nd arg is for logic
        os.makedirs(destination_folder, exist_ok=True) #access and define source_folder this is why we import os
    
        
        # Check file.filename not path.filename to verify extension
        file_type = file.filename.split(".")[-1].lower() # .split() at the "."
        image_name = os.path.splitext(file.filename)[0] # seperates name from ext
        image_bytes = file.file.read()           #needed for PIL? verify this
        image_file_path = os.path.join(source_folder, f"{image_name}.{file_type}") # conjoins indivudl pieces of abs path
        
    
        image = Image.open(io.BytesIO(image_bytes)).convert("RGBA")  # is is needed modify the images

         # check extensions list.
        if file_type not in ALLOWED:
            return (False, "Unsupported file type") #boolean needed for Exception
        
        if action == "convert":
            converted_path = os.path.join(destination_folder, f"{image_name}.png")
            image.save(converted_path, "PNG") # PIL working with images save(path, format/ext)
            return (True, "Image converted to PNG successfully")

            # Check logic based on img_type argument
            if action == "original": 
                #.save(destination_path, {file_type}) #path and format; format determined by file extension
                pass

            elif action == "thumbnail":
                #width, height = image.size
                #image.resize()
                #image.save(destination_path, {file_type}) #path and format; format determined by file extension
                pass
        
            

@app.post("/upload-image")
async def upload_image(
    file: UploadFile = File(...),
    action: str = "original"
):
   

    if not success:
        raise HTTPException(status_code=400, detail=message)

    return 

