import unittest
import os
import io
from PIL import Image
from fastapi import UploadFile
from fastapi.testclient import TestClient
from starlette.datastructures import UploadFile as StarletteUploadFile
from image_service import app
from image_service import image_channel


class TestImageService(unittest.TestCase):

    def setUp(self):
        # Create temporary folders for testing
        self.source_folder = "./test_source"
        self.dest_folder = "./test_destination"
        self.client = TestClient(app)    # specifically to test API clls

        os.makedirs(self.source_folder, exist_ok=True)
        os.makedirs(self.dest_folder, exist_ok=True)

        # Create a small in-memory image
        img = Image.new("RGB", (100, 100), color="red")
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="JPEG")
        img_bytes.seek(0)

        #  create image file object
        self.test_file = StarletteUploadFile(
            filename="test.jpg",
            file=img_bytes
        )

    def tearDown(self):
        # Clean up created files and folders
        for folder in [self.source_folder, self.dest_folder]:
            if os.path.exists(folder):
                for file in os.listdir(folder):
                    os.remove(os.path.join(folder, file))
                os.rmdir(folder)

    def test_convert(self):
        success, message = image_channel(
            self.source_folder,
            self.dest_folder,
            self.test_file,
            "convert"
        )

        # Assert success returned
        self.assertTrue(success)
        self.assertEqual(message, "Image converted to PNG successfully")

        # Assert converted file exists
        converted_path = os.path.join(self.dest_folder, "test.png")
        self.assertTrue(os.path.exists(converted_path))

    def test_original(self):
        success, message = image_channel(
            self.source_folder,
            self.dest_folder,
            self.test_file,
            "original"
        )

        # Assert success returned
        self.assertTrue(success)
        self.assertEqual(message, "Image saved successfully")

        # Assert converted file exists
        converted_path = os.path.join(self.dest_folder, "test.jpg")
        self.assertTrue(os.path.exists(converted_path))


    def test_thumbnail(self):
        success, message = image_channel(
            self.source_folder,
            self.dest_folder,
            self.test_file,
            "thumbnail"
        )

        # Assert success returned
        self.assertTrue(success) # assertTrue checks if "sucess" is true
        self.assertEqual(message, "Thumbnail created successfully")

        # Assert converted file exists
        converted_path = os.path.join(self.dest_folder, "test_thumbnail.jpg")
        self.assertTrue(os.path.exists(converted_path))  # .exist checks if soemthing exists, assertTrue checks if true


    def test_get(self):
        image_channel(self.source_folder, self.dest_folder, self.test_file, "original")
       
        #responose converts json response to python
        get_response = self.client.get(f"/fetch-image/test", params={"destination_folder": self.dest_folder})

        # accert comparison
        self.assertEqual(get_response.status_code, 200)
        data = get_response.json()
        self.assertTrue(data["success"]) # assertTrue checks if the date retruns "sucess" and if True nothing happens if False an error appears
        self.assertEqual(data["filename"], "test.jpg") # comapares filename and test.jpg to make sure they are the same.


    def test_delete(self):
        success, message = image_channel(self.source_folder, self.dest_folder, self.test_file, "original")

        file_path = os.path.join(self.dest_folder, "test.jpg") # create path for next assert
        self.assertTrue(os.path.exists(file_path))  # check if it exists

        # need this info so get the response data
        delete_response= self.client.delete(f"/delete-image/test", params={"destination_folder": self.dest_folder})

        self.assertEqual(delete_response.status_code, 200)
        data = delete_response.json()
       
        #responose converts json response to python
        self.assertTrue(data["success"])
        self.assertEqual(data["message"], "Image test.jpg deleted successfully")

        # accert comparison
        deleted_path = os.path.join(self.dest_folder, "test.jpg")
        self.assertFalse(os.path.exists(deleted_path))


if __name__ == "__main__":
    unittest.main()