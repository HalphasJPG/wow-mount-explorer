import os
import requests
from dotenv import load_dotenv

# 1. Ladda inställningar från .env
load_dotenv()

def get_access_token():
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    
    url = "https://oauth.battle.net/token"
    data = {'grant_type': 'client_credentials'}
    
    # Fråga Blizzard om lov
    response = requests.post(url, data=data, auth=(client_id, client_secret))
    
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        print(f"Fel vid hämtning av token: {response.status_code}")
        return None

def get_wow_mounts(token):
    # Adressen till mount-listan
    url = "https://eu.api.blizzard.com/data/wow/mount/index"
    
    params = {
        "namespace": "static-eu",
        "locale": "en_GB"
    }
    headers = {
        "Authorization": f"Bearer {token}"
    }

    print("Hämtar mounts från Blizzard...")
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()['mounts']
    else:
        print(f"Kunde inte hämta mounts: {response.status_code}")
        return []

# --- HÄR STARTAR PROGRAMMET ---
# Först hämtar vi ett "pass" (token)
my_token = get_access_token()

if my_token:
    # Sen använder vi passet för att hämta mounts
    all_mounts = get_wow_mounts(my_token)
    
    if all_mounts:
        print(f"\nSuccé! Hittade {len(all_mounts)} mounts.")
        print("Här är de första 10 i listan:")
        print("-" * 30)
        
        for mount in all_mounts[:10]:
            print(f"• {mount['name']}")