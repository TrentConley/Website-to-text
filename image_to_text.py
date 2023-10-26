from google.cloud import vision_v1
from google.cloud.vision_v1 import types
import io
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(
    os.getcwd(), "recipe-grocery-8d7eb704189f.json"
)


def convert_image_to_text(image_name, image_folder="images/", text_folder="text/"):
    print("attempting to read image.")
    # Initialize the Vision API client
    client = vision_v1.ImageAnnotatorClient()

    # Read the image file
    with io.open(image_folder + image_name + ".png", "rb") as image_file:
        content = image_file.read()

    image = vision_v1.Image(content=content)
    print("detecting text")
    # Perform text detection
    response = client.text_detection(image=image)
    texts = response.text_annotations
    print("detected text.")
    # Extracting text from the first annotation which contains the entire string
    extracted_text = texts[0].description if texts else ""

    # Create a .txt file with the same name as the image
    txt_file_path = os.path.splitext(image_name)[0] + ".txt"
    with open(text_folder + txt_file_path, "w") as f:
        f.write(extracted_text)

    print(f"Text written to {txt_file_path}")
