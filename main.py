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
    def get_wow_mounts(access_token):
    # Detta är adressen till listan över alla mounts
    url = "https://eu.api.blizzard.com/data/wow/mount/index"
    
    # Vi måste berätta för Blizzard vilken region (namespace) och vilket pass (token) vi har
    params = {
        "namespace": "static-eu",
        "locale": "en_GB"
    }
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    print("Hämtar mounts från Blizzard...")
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data['mounts'] # Returnerar själva listan
    else:
        print(f"Kunde inte hämta mounts. Felkod: {response.status_code}")
        return []

# Använd token vi fick tidigare för att hämta listan
mounts = get_wow_mounts(token)

if mounts:
    print(f"Hittade totalt {len(mounts)} mounts i World of Warcraft!")
    # Visa bara de 5 första så vi inte fyller hela terminalen
    print("Här är några exempel:")
    for mount in mounts[:5]:
        print(f"- {mount['name']}")