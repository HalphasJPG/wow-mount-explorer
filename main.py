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
    url = f"https://eu.api.blizzard.com/data/wow/mount/{mount_id}"
    params = {"namespace": "static-eu", "locale": "en_GB"}
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers, params=params)
    return response.json() if response.status_code == 200 else None

def get_wow_mounts(token):
    url = "https://eu.api.blizzard.com/data/wow/mount/index"
    params = {"namespace": "static-eu", "locale": "en_GB"}
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers, params=params)
    return response.json().get('mounts', []) if response.status_code == 200 else []

# --- Main Application Loop ---
token = get_access_token()

if token:
    mount_list = get_wow_mounts(token)
    
    if mount_list:
        print("\n--- TILLGÄNGLIGA MOUNTS (Första 10) ---")
        # Vi sparar de första 10 i en liten lista så vi kan matcha ID senare
        preview_list = mount_list[:10]
        
        for index, mount in enumerate(preview_list):
            print(f"{index + 1}. {mount['name']}")
        
        # Fråga användaren
        val = input("\nSkriv numret på den mount du vill se detaljer om (1-10): ")
        
        try:
            val_int = int(val) - 1 # Vi drar bort 1 eftersom listor börjar på 0
            if 0 <= val_int < 10:
                selected_mount = preview_list[val_int]
                mount_id = selected_mount['id']
                
                # Hämta detaljerna för den valda mounten
                details = get_mount_details(token, mount_id)
                
                if details:
                    print(f"\n--- INFO OM {details['name'].upper()} ---")
                    print(f"Beskrivning: {details.get('description', 'Ingen beskrivning tillgänglig.')}")
                    print(f"Källa: {details.get('source', {}).get('name', 'Okänd källa')}")
            else:
                print("Ogiltigt val, välj en siffra mellan 1 och 10.")
        except ValueError:
            print("Du måste skriva en siffra!")