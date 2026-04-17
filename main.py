import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_access_token():
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    
    # Blizzards adress för att få tillgång
    url = "https://oauth.battle.net/token"
    
    # Information som Blizzard kräver
    data = {'grant_type': 'client_credentials'}
    
    # Vi skickar ID och Secret för att bevisa vilka vi är
    response = requests.post(url, data=data, auth=(client_id, client_secret))
    
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        print(f"Fel vid hämtning av token: {response.status_code}")
        return None

# Testa funktionen
token = get_access_token()
if token:
    print("Succé! Vi har fått ett 'pass' (Access Token) från Blizzard!")
    print(f"Token börjar med: {token[:10]}...")