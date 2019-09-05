import pytesseract
from PIL import Image

jpg = "./1.jpg"
image = Image.open(jpg)
print(pytesseract.image_to_string(image))