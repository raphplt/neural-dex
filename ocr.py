import cv2
import pytesseract
from spellchecker import SpellChecker

spell = SpellChecker(language='fr')

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, threshold_img = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    morph_img = cv2.morphologyEx(threshold_img, cv2.MORPH_CLOSE, kernel)
    return morph_img

def extract_text_from_image(image_path):
    processed_image = preprocess_image(image_path)
    text = pytesseract.image_to_string(processed_image, lang="fra")
    return text

def correct_text(text):
    corrected_words = [spell.correction(word) for word in text.split()]
    corrected_words = [word for word in corrected_words if word is not None]
    return ' '.join(corrected_words)