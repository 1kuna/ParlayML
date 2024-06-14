import sqlite3
import json
import os

# Constants
BASE_DIR = 'k:/iCloudDrive/Git/KUNA/ParlayML'
DB_PATH = os.path.join(BASE_DIR, 'game_ids.db')
GAME_IDS_DIR = os.path.join(BASE_DIR, 'game_ids')

# Connect to the database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create table for game IDs if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS game_ids (
    game_id INTEGER PRIMARY KEY
)''')

# Function to load game IDs from JSON files and insert into the database
def load_and_insert_game_ids(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r') as file:
                game_ids = json.load(file)
                for game_id in game_ids:
                    cursor.execute('INSERT OR REPLACE INTO game_ids (game_id) VALUES (?)', (game_id,))
    conn.commit()

# Load game IDs and insert into the database
load_and_insert_game_ids(GAME_IDS_DIR)

# Close the connection
conn.close()
print('Game IDs successfully inserted into the database.')
