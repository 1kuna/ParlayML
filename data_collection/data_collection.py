import requests
import pandas as pd
import json
import os
from datetime import datetime

# Constants
DATA_DIR = 'data'
API_KEYS = {
    'sportsdataio': '7ab025ce69074cfda9bc955fb3803503',
    'api_sports': 'c93e31db582b233de7abed978cde6028',
    'mysportsfeeds': 'a0b19913-fcd3-4974-810d-687879'
}

API_URLS = {
    'sportsdataio': 'https://api.sportsdata.io/v3/nba/scores/json',
    'api_sports': 'https://v1.basketball.api-sports.io',
    'mysportsfeeds': 'https://api.mysportsfeeds.com/v2.1/pull/nba'
}

CURRENT_API = 'sportsdataio'

def fetch_data_sportsdataio(date):
    url = f"{API_URLS['sportsdataio']}/GamesByDate/{date}"
    headers = {'Ocp-Apim-Subscription-Key': API_KEYS['sportsdataio']}
    response = requests.get(url, headers=headers)
    print(f"Fetching data from SportsDataIO with URL: {url}")
    return response

def fetch_data_api_sports(date):
    url = f"{API_URLS['api_sports']}/games?date={date}"
    headers = {'x-apisports-key': API_KEYS['api_sports']}
    response = requests.get(url, headers=headers)
    print(f"Fetching data from API-Sports with URL: {url}")
    return response

def fetch_data_mysportsfeeds(date):
    url = f"{API_URLS['mysportsfeeds']}/games.json?date={date}"
    headers = {'Authorization': f"Basic {API_KEYS['mysportsfeeds']}"}
    response = requests.get(url, headers=headers)
    print(f"Fetching data from MySportsFeeds with URL: {url}")
    return response

def fetch_data(date):
    if CURRENT_API == 'sportsdataio':
        response = fetch_data_sportsdataio(date)
    elif CURRENT_API == 'api_sports':
        response = fetch_data_api_sports(date)
    elif CURRENT_API == 'mysportsfeeds':
        response = fetch_data_mysportsfeeds(date)
    
    if response.status_code == 429:  # Rate limit exceeded
        print(f"Rate limit exceeded for {CURRENT_API}. Switching API...")
        switch_api()
        return fetch_data(date)
    elif response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data from {CURRENT_API}. Status code: {response.status_code}")
        return None

def switch_api():
    global CURRENT_API
    apis = list(API_KEYS.keys())
    current_index = apis.index(CURRENT_API)
    CURRENT_API = apis[(current_index + 1) % len(apis)]
    print(f"Switched to {CURRENT_API}")

def save_data(data, filename):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Data saved to {filepath}")

def load_data(filename):
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            data = json.load(file)
        return data
    else:
        print(f"File {filename} does not exist.")
        return None

def process_game_data(game_data):
    games = []
    for game in game_data:
        game_info = {
            'game_id': game.get('GameID', game.get('id')),
            'date': datetime.strptime(game.get('DateTime', game.get('date')), '%Y-%m-%dT%H:%M:%S'),
            'home_team': game.get('HomeTeam', game.get('home_team')),
            'away_team': game.get('AwayTeam', game.get('away_team')),
            'home_score': game.get('HomeTeamScore', game.get('home_score')),
            'away_score': game.get('AwayTeamScore', game.get('away_score')),
            'status': game.get('Status', game.get('status')),
            'injuries': game.get('Injuries', game.get('injuries', []))
        }
        games.append(game_info)
    df = pd.DataFrame(games)
    return df

def main():
    # Example endpoints for fetching today's game data
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    # Fetch game data
    game_data = fetch_data(date_str)
    if game_data:
        save_data(game_data, 'game_data.json')

    # Load and process game data
    loaded_game_data = load_data('game_data.json')
    if loaded_game_data:
        processed_game_data = process_game_data(loaded_game_data)
        print(processed_game_data.head())

if __name__ == "__main__":
    main()
