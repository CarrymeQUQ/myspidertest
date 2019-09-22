import pytesseract
from PIL import Image

jpg = "./20181229205022579.png"
image = Image.open(jpg)
print(pytesseract.image_to_string(image, lang="chi_sim"))
