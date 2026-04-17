import os
import requests
from dotenv import load_dotenv
from datetime import datetime  # Ny import!

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

# --- Main Application ---
token = get_access_token()

if token:
    # Hämtar dagens datum och tid
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    all_mounts = get_wow_mounts(token)
    
    print(f"Welcome to WoW Mount Explorer!")
    print(f"Session started at: {now}") # Visar tiden för läraren

    while True:
        print("\n" + "-"*30)
        search_term = input("Search for a mount (or type 'exit'): ").lower()
        
        if search_term == 'exit':
            print("Closing program. Goodbye!")
            break
            
        results = [m for m in all_mounts if search_term in m['name'].lower()]
        
        if results:
            print(f"\nFound {len(results)} matches (showing top 15):")
            for i, m in enumerate(results[:15]):
                print(f"{i+1}. {m['name']}")
                
            val = input("\nEnter number for details or press Enter to search again: ")
            
            if val.isdigit():
                val_int = int(val) - 1
                if 0 <= val_int < len(results[:15]):
                    selected = results[val_int]
                    details = get_mount_details(token, selected['id'])
                    
                    if details:
                        print("\n" + "="*45)
                        print(f"  {details['name'].upper()}")
                        print("="*45)
                        print(f"Description: {details.get('description', 'N/A')}")
                        print(f"Source:      {details.get('source', {}).get('name', 'Unknown')}")
                        print(f"ID:          {details.get('id')}")
                        print("="*45)
                else:
                    print("Invalid selection.")
        else:
            print(f"No mounts found matching '{search_term}'.")