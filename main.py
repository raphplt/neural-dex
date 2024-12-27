from fastapi import FastAPI, UploadFile, File
from ocr import extract_text_from_image, correct_text
from api_caller import search_pokemon_card
import logging
import json
import re

app = FastAPI()
logging.basicConfig(level=logging.INFO)

def load_pokemon_names(file_path="pokemon_names.json"):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

pokemon_names = load_pokemon_names()

def match_pokemon_name(extracted_text, pokemon_names):
    corrected_text = correct_text(extracted_text)
    for name in pokemon_names:
        if name.lower() in corrected_text.lower():
            return name
    return "Unknown"

def extract_card_number(extracted_text):
    match = re.search(r"\b\d{3}\b", extracted_text)
    return match.group() if match else "Unknown"

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    file_location = f"test_images/{file.filename}"
    
    with open(file_location, "wb") as f:
        f.write(await file.read())
    logging.info(f"File saved at: {file_location}")
    
    extracted_text = extract_text_from_image(file_location)
    logging.info(f"Extracted text: {extracted_text}")
    
    pokemon_name = match_pokemon_name(extracted_text, pokemon_names)
    pokemon_number = extract_card_number(extracted_text)
    logging.info(f"Detected name: {pokemon_name}, number: {pokemon_number}")
    
    api_result = search_pokemon_card(pokemon_name, pokemon_number)
    return {"extracted_text": extracted_text, "pokemon_name": pokemon_name, "pokemon_number": pokemon_number, "api_result": api_result}