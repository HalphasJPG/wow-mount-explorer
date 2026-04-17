# WoW Mount Explorer 🐉

A Python-based command-line interface (CLI) tool that allows users to explore the vast library of mounts in World of Warcraft. The application fetches real-time data directly from the official Blizzard Game Data API.

## Features
- **OAuth2 Authentication:** Securely retrieves Access Tokens from Blizzard's servers.
- **Advanced Search:** Filter through over 900+ mounts using keywords.
- **Detailed Data Extraction:** View descriptions, sources, and IDs.
- **Session Timestamps:** Displays when the search session started.
- **Robust Error Handling:** Validates user input to prevent crashes.
- **Interactive Loop:** Allows for continuous searching until exit.

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