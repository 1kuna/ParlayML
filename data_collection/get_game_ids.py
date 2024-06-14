import requests
import json
import os

# Replace with your actual API key
API_KEY = '7ab025ce69074cfda9bc955fb3803503'
# Define the season range you want to fetch
for SEASON in range(2021, 2022):
    # Define the URL for the game schedule
    URL = f'https://api.sportsdata.io/v3/nba/scores/json/Games/{SEASON}?key={API_KEY}'

    # Make the API request
    response = requests.get(URL)

    if response.status_code == 200:
        games = response.json()
        
        # Extract all game IDs
        game_ids = [game['GameID'] for game in games]
        
        # Define the file path in the local directory
        file_path = os.path.join(os.getcwd(), f'game_ids_{SEASON}.json')
        
        # Save the game IDs to a file in the local directory
        with open(file_path, 'w') as file:
            json.dump(game_ids, file, indent=4)
        
        print(f'Successfully exported {len(game_ids)} game IDs to {file_path}')
    else:
        print(f'Failed to fetch game data. Status code: {response.status_code}')
        print(response.text)
