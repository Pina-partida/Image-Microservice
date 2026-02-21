## Image Microservice

- Image File Verification and Modification Microservice

## Description
- A microservice that confirms image file type and assists with formatting images. THis microservice utilizes FastAPI as a communication endpoint and (PIL) for image modification.

## Contributors
- Teodoro Partida Valencia
- Samuel Vernick
- Sarah Van Hoose

## Communication Contract
- Our main method of communication will be our Discord Server.
- We are expected to respond within 48 hours.
- In case of upcoming deadlines and a team member is not reachable through Discord for 48 hours, the remaining team members will attempt to contact the team member through Microsoft Teams or university email. If the team member is still not reachable within 24 hours, the remaining team members will convene to decide next steps.
- Virtual meeting can be requested by any team member if they deem it necessary. Only one additional teammate needs to approve this meeting for it to procced.
- Work on a microservice should be reasonably split.


## API Endpoints
- POST /upload-image
- multipart/form-data

## Parameters
- Name	Type	Required	Description
- file	File	Yes	Image file to upload
- action	String	No	Processing action (original, convert, thumbnail)
- import requests

## Example Request
url = "http://localhost:8000/upload-image"

files = {
    "file": open("example.jpg", "rb")
}

data = {
    "action": "convert"
}

response = requests.post(url, files=files, data=data)

print(response.status_code)
print(response.json())

## Example Success 200 ok
{
    "message": "Image converted to PNG successfully"
}

## Example Error 400
{
    "detail": "Unsupported file type"
}

## Response HAndling
if response.status_code == 200:
    print("Success:", response.json()["message"])
else:
    print("Error:", response.json()["detail"])
