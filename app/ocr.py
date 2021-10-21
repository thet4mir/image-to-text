from .settings import BASE_DIR
import pytesseract
import pathlib
from PIL import Image

IMG_DIR = BASE_DIR / "images"
img_path = IMG_DIR / "ingredeients-1.png"

img = Image.open(img_path)
preds = pytesseract.image_to_string(img)
predictions = [x for x in preds.split("\n")]

print(predictions)
