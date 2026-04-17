import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_access_token():
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    url = "https://oauth.battle.net/token"
    data = {'grant_type': 'client_credentials'}
    response = requests.post(url, data=data, auth=(client_id, client_secret))
    return response.json().get('access_token') if response.status_code == 200 else None

def get_mount_details(token, mount_id):
    # Ny adress som går direkt på ett specifikt ID
    url = f"https://eu.api.blizzard.com/data/wow/mount/{mount_id}"
    params = {"namespace": "static-eu", "locale": "en_GB"}
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers, params=params)
    return response.json() if response.status_code == 200 else None

# --- Huvudprogram ---
token = get_access_token()
if token:
    # Vi testar att hämta detaljer för mount ID 6 (vilket råkar vara 'Brown Horse')
    print("Hämtar detaljer för en specifik mount...")
    details = get_mount_details(token, 6)
    
    if details:
        print("\n--- MOUNT DETALJER ---")
        print(f"Namn: {details.get('name')}")
        print(f"Beskrivning: {details.get('description')}")
        print(f"Källa: {details.get('source', {}).get('name')}")
        print(f"Typ: {details.get('creature_displays', [{}])[0].get('id')} (ID)")