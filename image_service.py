from fastapi import FastAPI, UploadFile, File, HTTPException
from PIL import Image
import os
import io
# dont use pathlib from Path because user will define directories

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
        image_bytes = file.file.read()           #needed for PIL to process
        image_file_path = os.path.join(source_folder, f"{image_name}.{file_type}") # conjoins indivudl pieces of abs path
        
    
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB") # is is needed modify the images dont use RGBA cuass failures due to conversion

         # check extensions list.
        if file_type not in ALLOWED:
            return (False, "Unsupported file type") #boolean needed for Exception
        
        # Save the original image to source_folder
        image.save(image_file_path, file_type.upper() if file_type != "jpg" else "JPEG")
        
        # Check logic based on action argument
        if action == "convert":
            converted_path = os.path.join(destination_folder, f"{image_name}.png")
            image.save(converted_path, "PNG") # PIL working with images save(path, format/ext)
            return (True, "Image converted to PNG successfully")

        elif action == "original": 
            original_path = os.path.join(destination_folder, f"{image_name}.{file_type}")
            image.save(original_path, file_type.upper() if file_type != "jpg" else "JPEG") # saves image in original formatting to destination folder
            return (True, "Image saved successfully")
        
        elif action == "thumbnail":
            width, height = image.size
            thumbnail_size = (200, 200) # sets max size to 200 px by 200 px
            image.thumbnail(thumbnail_size, Image.Resampling.LANCZOS) # shrinks image proportinally to fit 200x200 using LANCZOS (high quality resampling)
            thumbnail_path = os.path.join(destination_folder, f"{image_name}_thumbnail.{file_type}")
            image.save(thumbnail_path, file_type.upper() if file_type != "jpg" else "JPEG") # saves thumbnail with _thumbnail suffix before the extension
            return (True, "Thumbnail created successfully")
        
    except Exception as e:
        return (False, f"Error processing image: {str(e)}") # catch any error and return failure tuple with error message

@app.post("/upload-image")
async def upload_image(
    file: UploadFile = File(...),
    action: str = "original",
    source_folder: str = "./images/source",
    destination_folder: str = "./images/destination"
):
    success, message = image_channel(source_folder, destination_folder, file, action) # unpacks the success message
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    return {"success": True, "message": message, "image_name": file.filename}


@app.get("/fetch-image/{image_name}")
async def fetch_image(
    image_name: str,
    destination_folder: str = "./images/destination"
):
    """Retrive a processed image from the destination folder"""
    try:
        # Try and find the image file
        for file in os.listdir(destination_folder):
            if file.startswith(image_name): # catches thumbnails and converted versions
                file_path = os.path.join(destination_folder, file) 
                return {"success": True, "file_path": file_path, "filename": file}
            
        raise HTTPException(status_code=404, detail="Image not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving image: {str(e)}")
    

@app.delete("/delete-image/{image_name}")
async def delete_image(
    image_name: str,
    destination_folder: str = "./images/destination"
):
    """Delete an image from the destination folder"""
    try:
        # Try and delete the image file
        for file in os.listdir(destination_folder):
            if file.startswith(image_name): # catches thumbnails and converted versions
                file_path = os.path.join(destination_folder, file)
                os.remove(file_path)
                return {"success": True, "message": f"Image {file} deleted successfully"} # return success message if file successfully deleted
            
        raise HTTPException(status_code=404, detail="Image not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting image: {str(e)}")


