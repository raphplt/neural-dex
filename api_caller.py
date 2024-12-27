import requests
from dotenv import load_dotenv
import os

load_dotenv()

def search_pokemon_card(name, number):
    url = f"https://api.pokemontcg.io/v2/cards?q=name:{name}+number:{number}"
    api_key = os.getenv("API_KEY")
    headers = {"X-Api-Key": api_key}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data"}