import requests
import sqlite3
from dotenv import load_dotenv
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()

# Constants
BASE_DIR = os.getenv('BASE_DIR', '.')  # Use current directory as default
DB_PATH = os.path.join(BASE_DIR, 'game_ids.db')
NEW_DB_PATH = os.path.join(BASE_DIR, 'features.db')
API_KEY = os.getenv('SPORTSDATAIO_KEY')
API_URL = 'https://api.sportsdata.io/v3/nba/scores/json/Games'

if not API_KEY:
    logging.error('API_KEY not found. Please set it in the environment variables.')
    exit(1)

# Connect to the existing database
conn_old = sqlite3.connect(DB_PATH)
cursor_old = conn_old.cursor()

# Connect to the new database
conn_new = sqlite3.connect(NEW_DB_PATH)
cursor_new = conn_new.cursor()

def create_tables():
    cursor_new.execute('''
    CREATE TABLE IF NOT EXISTS player_performance (
        game_id INTEGER,
        player_id INTEGER,
        points REAL,
        rebounds REAL,
        assists REAL,
        efficiency REAL,
        PRIMARY KEY (game_id, player_id)
    )''')

    cursor_new.execute('''
    CREATE TABLE IF NOT EXISTS team_performance (
        game_id INTEGER,
        team_id INTEGER,
        offensive_efficiency REAL,
        defensive_efficiency REAL,
        win_rate REAL,
        home_away TEXT,
        PRIMARY KEY (game_id, team_id)
    )''')

    cursor_new.execute('''
    CREATE TABLE IF NOT EXISTS injuries (
        player_id INTEGER,
        status TEXT,
        PRIMARY KEY (player_id)
    )''')

def fetch_games_by_season(season):
    url = f'{API_URL}/{season}?key={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        logging.error(f'Failed to fetch games for season {season}. Status Code: {response.status_code}, Response: {response.text}')
        return None

def fetch_injury_data():
    url = f'{API_URL}/Injuries?key={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        logging.error(f'Failed to fetch injury data. Status Code: {response.status_code}, Response: {response.text}')
        return None

def save_player_performance(game_id, player_data):
    for player in player_data:
        cursor_new.execute('''
            INSERT OR REPLACE INTO player_performance (game_id, player_id, points, rebounds, assists, efficiency)
            VALUES (?, ?, ?, ?, ?, ?)''', 
            (game_id, player['PlayerID'], player['Points'], player['Rebounds'], player['Assists'], player['Efficiency']))

def save_team_performance(game_id, team_data):
    for team in team_data:
        cursor_new.execute('''
            INSERT OR REPLACE INTO team_performance (game_id, team_id, offensive_efficiency, defensive_efficiency, win_rate, home_away)
            VALUES (?, ?, ?, ?, ?, ?)''', 
            (game_id, team['TeamID'], team['OffensiveEfficiency'], team['DefensiveEfficiency'], team['WinRate'], team['HomeAway']))

def save_injuries(injury_data):
    for player in injury_data:
        cursor_new.execute('''
            INSERT OR REPLACE INTO injuries (player_id, status)
            VALUES (?, ?)''', 
            (player['PlayerID'], player['Status']))

def process_game_data(game_ids, all_games):
    for game_id in game_ids:
        game_id = game_id[0]
        logging.info(f"Processing game ID: {game_id}")
        
        game_data = next((game for game in all_games if game['GameID'] == game_id), None)
        
        if game_data:
            player_data = game_data.get('PlayerStats', [])
            save_player_performance(game_id, player_data)
            
            team_data = game_data.get('TeamStats', [])
            save_team_performance(game_id, team_data)
        else:
            logging.warning(f'Game data not found for game ID {game_id}')

def main():
    create_tables()
    
    cursor_old.execute('SELECT game_id FROM game_ids')
    game_ids = cursor_old.fetchall()
    
    seasons = [2021, 2022]  # Add more seasons as needed
    all_games = []
    for season in seasons:
        season_games = fetch_games_by_season(season)
        if season_games:
            all_games.extend(season_games)

    process_game_data(game_ids, all_games)
    
    injury_data = fetch_injury_data()
    if injury_data:
        save_injuries(injury_data)

    conn_new.commit()
    conn_new.close()
    conn_old.close()
    logging.info('Data successfully saved to the new database.')

if __name__ == '__main__':
    main()
