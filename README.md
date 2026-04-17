# WoW Mount Explorer 🐉

A Python-based command-line interface (CLI) tool that allows users to explore the vast library of mounts in World of Warcraft. The application fetches real-time data directly from the official Blizzard Game Data API.

## Features
- **Secure Authentication:** Implements OAuth2 protocol to retrieve Access Tokens from Blizzard.
- **Search & Filter:** Search by name (e.g., "Drake" or "Horse") across a database of 900+ mounts.
- **Detailed View:** Provides descriptions, sources (how to obtain the mount), and unique IDs for each selection.
- **Data Security:** Uses `.env` files to keep sensitive API credentials out of the source code.
- **Interactive Loop:** Allows for continuous searching without restarting the application.
- Session timestamps and robust error handling

## Data Source
All data provided by this application is fetched from the **Blizzard Entertainment API**. This project uses the:
- [Mount API](https://develop.battle.net/documentation/world-of-warcraft/game-data-apis)
- [OAuth2 API](https://develop.battle.net/documentation/guides/using-oauth)

## Installation & Usage

### 1. Prerequisites
You need Python installed and your own API credentials from the [Battle.net Developer Portal](https://develop.battle.net/).

### 2. Configure Environment Variables
Create a file named `.env` in the root directory and add your keys:
```env
CLIENT_ID=your_id_here
CLIENT_SECRET=your_secret_here