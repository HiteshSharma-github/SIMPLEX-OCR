import base64

import numpy as np
import pytesseract
from django.contrib import messages
from django.shortcuts import render
from PIL import Image, ImageFilter, ImageEnhance

# you have to install tesseract module too from here - https://github.com/UB-Mannheim/tesseract/wiki
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Path to tesseract.exe
)


def homepage(request):
    if request.method == "POST":
        try:
            image = request.FILES["imagefile"]
            # encode image to base64 string
            image_base64 = base64.b64encode(image.read()).decode("utf-8")
        except:
            messages.add_message(
                request, messages.ERROR, "No image selected or uploaded"
            )
            return render(request, "home.html")
        lang = request.POST["language"]
        # Open image with PIL and apply filters
        img = Image.open(image)
        img = img.convert("L")  # Convert to grayscale
        img = img.filter(ImageFilter.SHARPEN)  # Sharpen the image
        img = ImageEnhance.Contrast(img).enhance(2)  # Increase the contrast
        img = np.array(img)  # Convert PIL image to numpy array
        text = pytesseract.image_to_string(img, lang=lang)
        # return text to html
        return render(request, "home.html", {"ocr": text, "image": image_base64})

    return render(request, "home.html")