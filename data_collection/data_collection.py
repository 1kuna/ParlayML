import requests
import pandas as pd
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Constants
DATA_DIR = 'data'
API_KEYS = {
    'sportsdataio': os.getenv('SPORTSDATAIO_KEY'),
    'api_sports': os.getenv('API_SPORTS_KEY'),
    'mysportsfeeds': os.getenv('MYSPORTSFEEDS_KEY')
}

API_URLS = {
    'sportsdataio': 'https://api.sportsdata.io/v3/nba/stats/json',
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

def fetch_injury_data_sportsdataio():
    url = 'https://api.sportsdata.io/v3/nba/stats/json/Injuries'
    headers = {'Ocp-Apim-Subscription-Key': API_KEYS['sportsdataio']}
    response = requests.get(url, headers=headers)
    print(f"Fetching injury data from SportsDataIO with URL: {url}")
    return response

def fetch_data_api_sports(date):
    url = f"{API_URLS['api_sports']}/games?date={date}"
    headers = {'x-apisports-key': API_KEYS['api_sports']}
    response = requests.get(url, headers=headers)
    print(f"Fetching data from API-Sports with URL: {url}")
    return response

def fetch_injury_data_api_sports():
    url = f"{API_URLS['api_sports']}/injuries"
    headers = {'x-apisports-key': API_KEYS['api_sports']}
    response = requests.get(url, headers=headers)
    print(f"Fetching injury data from API-Sports with URL: {url}")
    return response

def fetch_data_mysportsfeeds(date):
    url = f"{API_URLS['mysportsfeeds']}/games.json?date={date}"
    headers = {'Authorization': f"Basic {API_KEYS['mysportsfeeds']}"}
    response = requests.get(url, headers=headers)
    print(f"Fetching data from MySportsFeeds with URL: {url}")
    return response

def fetch_injury_data_mysportsfeeds():
    url = f"{API_URLS['mysportsfeeds']}/injuries.json"
    headers = {'Authorization': f"Basic {API_KEYS['mysportsfeeds']}"}
    response = requests.get(url, headers=headers)
    print(f"Fetching injury data from MySportsFeeds with URL: {url}")
    return response

def fetch_data(date):
    global CURRENT_API
    apis = ['sportsdataio', 'api_sports', 'mysportsfeeds']
    
    for api in apis:
        CURRENT_API = api
        if api == 'sportsdataio':
            response = fetch_data_sportsdataio(date)
        elif api == 'api_sports':
            response = fetch_data_api_sports(date)
        elif api == 'mysportsfeeds':
            response = fetch_data_mysportsfeeds(date)
        
        if response.status_code == 200 and response.json():
            return response.json()
        else:
            print(f"Failed to fetch data from {api} API. Trying next API...")
    
    print("All APIs failed to fetch data.")
    return None

def fetch_injury_data():
    global CURRENT_API
    apis = ['sportsdataio', 'api_sports', 'mysportsfeeds']
    
    for api in apis:
        CURRENT_API = api
        if api == 'sportsdataio':
            response = fetch_injury_data_sportsdataio()
        elif api == 'api_sports':
            response = fetch_injury_data_api_sports()
        elif api == 'mysportsfeeds':
            response = fetch_injury_data_mysportsfeeds()
        
        if response.status_code == 200 and response.json() and not 'errors' in response.json():
            return response.json()
        else:
            print(f"Failed to fetch injury data from {api} API. Trying next API...")
    
    print("All APIs failed to fetch injury data.")
    return None

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

def process_injury_data(injury_data):
    print(injury_data)  # Debugging step to inspect the structure of injury_data
    injuries = []
    for injury in injury_data:
        if isinstance(injury, dict):
            injury_info = {
                'player_id': injury.get('PlayerID'),
                'player_name': injury.get('Name'),
                'team': injury.get('Team'),
                'position': injury.get('Position'),
                'injury': injury.get('Injury'),
                'status': injury.get('Status'),
                'date': datetime.strptime(injury.get('Updated'), '%Y-%m-%dT%H:%M:%S')
            }
            injuries.append(injury_info)
    df = pd.DataFrame(injuries)
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

    # Fetch injury data
    injury_data = fetch_injury_data()
    if injury_data:
        save_data(injury_data, 'injury_data.json')

    # Load and process injury data
    loaded_injury_data = load_data('injury_data.json')
    if loaded_injury_data:
        processed_injury_data = process_injury_data(loaded_injury_data)
        print(processed_injury_data.head())

if __name__ == "__main__":
    main()