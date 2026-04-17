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

# --- Main Application ---
token = get_access_token()

if token:
    all_mounts = get_wow_mounts(token)
    
    print("--- WoW Mount Sök ---")
    search_term = input("Sök efter en mount (t.ex. 'Drake' eller 'Horse'): ").lower()
    
    # Här filtrerar vi listan manuellt - detta är jättebra att visa läraren!
    results = [m for m in all_mounts if search_term in m['name'].lower()]
    
    if results:
        print(f"\nHittade {len(results)} matchningar:")
        for i, m in enumerate(results[:15]): # Visa max 15 träffar
            print(f"{i+1}. {m['name']}")
            
        val = input("\nVilken vill du veta mer om? (nummer): ")
        try:
            selected = results[int(val)-1]
            details = get_mount_details(token, selected['id'])
            if details:
                print(f"\n--- {details['name'].upper()} ---")
                print(f"Beskrivning: {details.get('description', 'Saknas')}")
                print(f"Källa: {details.get('source', {}).get('name', 'Okänd')}")
        except:
            print("Det där gick inte riktigt, försök igen!")
    else:
        print("Inga mounts hittades med det namnet.")