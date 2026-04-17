"""
WoW Mount Explorer
Author: HalphasJPG
Version: 1.0
Description: A tool to explore World of Warcraft mounts via Blizzard API.
"""

import os
import requests
from dotenv import load_dotenv
from datetime import datetime

# --- Configuration & Setup ---
load_dotenv()

def get_access_token():
    """Retrieves an OAuth2 access token from Blizzard."""
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    url = "https://oauth.battle.net/token"
    data = {'grant_type': 'client_credentials'}
    
    try:
        response = requests.post(url, data=data, auth=(client_id, client_secret))
        return response.json().get('access_token') if response.status_code == 200 else None
    except Exception as e:
        print(f"Connection error: {e}")
        return None

def get_wow_mounts(token):
    """Fetches the full index of mounts from the game data API."""
    url = "https://eu.api.blizzard.com/data/wow/mount/index"
    params = {"namespace": "static-eu", "locale": "en_GB"}
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers, params=params)
    return response.json().get('mounts', []) if response.status_code == 200 else []

def get_mount_details(token, mount_id):
    """Fetches specific details for a single mount ID."""
    url = f"https://eu.api.blizzard.com/data/wow/mount/{mount_id}"
    params = {"namespace": "static-eu", "locale": "en_GB"}
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers, params=params)
    return response.json() if response.status_code == 200 else None

# --- Main Application Logic ---
token = get_access_token()

if token:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    all_mounts = get_wow_mounts(token)
    
    print(f"Welcome to WoW Mount Explorer!")
    print(f"Session started at: {now}")

    while True:
        print("\n" + "-"*40)
        search_term = input("Search for a mount (or type 'exit' to quit): ").lower().strip()
        
        if search_term == 'exit':
            print("Closing application. Have a great day!")
            break
            
        if not search_term:
            continue

        # Filter the mount list based on search term
        results = [m for m in all_mounts if search_term in m['name'].lower()]
        
        if results:
            print(f"\nFound {len(results)} matches (showing top 15):")
            for i, m in enumerate(results[:15]):
                print(f"{i+1}. {m['name']}")
                
            val = input("\nEnter number for details or press Enter to search again: ")
            
            try:
                val_int = int(val) - 1
                if 0 <= val_int < len(results[:15]):
                    selected = results[val_int]
                    details = get_mount_details(token, selected['id'])
                    
                    if details:
                        print("\n" + "="*45)
                        print(f"  {details['name'].upper()}")
                        print("="*45)
                        print(f"Description: {details.get('description', 'No description available.')}")
                        print(f"Source:      {details.get('source', {}).get('name', 'Unknown')}")
                        print(f"Mount ID:    {details.get('id')}")
                        print("="*45)
                else:
                    print("Error: Selection out of range.")
            except ValueError:
                if val != "": # Ignore if user just pressed Enter
                    print("Error: Please enter a valid number.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
        else:
            print(f"No mounts found matching '{search_term}'.")