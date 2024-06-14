import json
import os
import sqlite3

# Constants
DB_PATH = 'sports_betting.db'
GAME_IDS_DIR = 'game_ids'  # Directory where game ID files are stored

def load_json_files(directory):
    all_data = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r') as file:
                data = json.load(file)
                all_data.extend(data if isinstance(data, list) else [data])
    return all_data

def save_to_db(data, table_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT NOT NULL
    )''')
    for item in data:
        cursor.execute(f'INSERT INTO {table_name} (data) VALUES (?)', (json.dumps(item),))
    conn.commit()
    conn.close()

def main():
    game_data = load_json_files(GAME_IDS_DIR)
    
    if game_data:
        save_to_db(game_data, 'game_data')
        print(f'Successfully saved {len(game_data)} records to the database.')

if __name__ == '__main__':
    main()
