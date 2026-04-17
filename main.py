import os
import requests
from dotenv import load_dotenv

# Ladda miljövariabler (API-nycklar)
load_dotenv()

def get_access_token():
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    url = "https://oauth.battle.net/token"
    data = {'grant_type': 'client_credentials'}
    response = requests.post(url, data=data, auth=(client_id, client_secret))
    return response.json().get('access_token') if response.status_code == 200 else None

def get_wow_mounts(token):
    url = "https://eu.api.blizzard.com/data/wow/mount/index"
    params = {"namespace": "static-eu", "locale": "en_GB"}
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers, params=params)
    return response.json().get('mounts', []) if response.status_code == 200 else []

def get_mount_details(token, mount_id):
    url = f"https://eu.api.blizzard.com/data/wow/mount/{mount_id}"
    params = {"namespace": "static-eu", "locale": "en_GB"}
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers, params=params)
    return response.json() if response.status_code == 200 else None

# --- Main Application Loop ---
token = get_access_token()

if token:
    all_mounts = get_wow_mounts(token)
    print("Välkommen till WoW Mount Explorer!")

    while True:
        print("\n" + "-"*30)
        search_term = input("Sök efter en mount (eller skriv 'exit' för att avsluta): ").lower()
        
        if search_term == 'exit':
            print("Avslutar programmet. Hejdå!")
            break
            
        # Filtrera listan baserat på sökning
        results = [m for m in all_mounts if search_term in m['name'].lower()]
        
        if results:
            print(f"\nHittade {len(results)} matchningar (visar topp 15):")
            for i, m in enumerate(results[:15]):
                print(f"{i+1}. {m['name']}")
                
            val = input("\nVilken vill du veta mer om? (nummer) eller tryck Enter för ny sökning: ")
            
            if val.isdigit():
                val_int = int(val) - 1
                if 0 <= val_int < len(results[:15]):
                    selected = results[val_int]
                    details = get_mount_details(token, selected['id'])
                    
                    if details:
                        print("\n" + "="*45)
                        print(f"  {details['name'].upper()}")
                        print("="*45)
                        print(f"Beskrivning: {details.get('description', 'Saknas')}")
                        print(f"Källa:       {details.get('source', {}).get('name', 'Okänd')}")
                        print(f"ID:          {details.get('id')}")
                        print("="*45)
                else:
                    print("Ogiltigt nummer.")
        else:
            print(f"Inga mounts hittades som matchar '{search_term}'.")