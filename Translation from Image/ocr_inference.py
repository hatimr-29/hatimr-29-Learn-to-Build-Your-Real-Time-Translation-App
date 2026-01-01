import cv2
import easyocr

# Create EasyOCR reader once
reader = easyocr.Reader(['en'], gpu=False)

def extract_text_from_image(image_bgr):
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    results = reader.readtext(image_rgb, detail=0)
    return " ".join(results)
