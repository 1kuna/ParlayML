
import sqlite3
import pandas as pd

def fetch_data_from_db(query):
    conn = sqlite3.connect('sports_betting.db')
    data = pd.read_sql_query(query, conn)
    conn.close()
    return data

def calculate_player_metrics():
    player_stats = fetch_data_from_db('SELECT * FROM PlayerStats')
    player_stats['efficiency'] = (player_stats['points_per_game'] +
                                  player_stats['assists_per_game'] +
                                  player_stats['rebounds_per_game']) / 3
    return player_stats

def calculate_team_metrics():
    team_stats = fetch_data_from_db('SELECT * FROM TeamStats')
    team_stats['win_rate'] = team_stats['wins'] / (team_stats['wins'] + team_stats['losses'])
    return team_stats

def main():
    player_metrics = calculate_player_metrics()
    team_metrics = calculate_team_metrics()
    print("Player Metrics:\n", player_metrics.head())
    print("Team Metrics:\n", team_metrics.head())

if __name__ == "__main__":
    main()


# Improvements


# Feature Engineering Improvements

# Advanced Feature Engineering
# - Introduce more sophisticated features, such as player fatigue, weather conditions, and venue-specific performance.
# - Address class imbalances in the dataset to improve model performance.

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

def load_data():
    # Example function to load data from a database or CSV file
    data = pd.read_csv('sports_data.csv')
    return data

def create_features(data):
    # Creating new features
    data['points_per_game'] = data['total_points'] / data['games_played']
    data['assists_per_game'] = data['total_assists'] / data['games_played']
    data['rebounds_per_game'] = data['total_rebounds'] / data['games_played']
    data['win_rate'] = data['wins'] / data['games_played']

    # New features for player fatigue and venue-specific performance
    data['player_fatigue'] = data['minutes_played'] / data['days_rest']
    data['home_venue_advantage'] = np.where(data['venue'] == 'home', 1, 0)

    # Convert categorical injury status to numerical
    data['injury_status'] = data['injury_status'].apply(lambda x: 0 if x == 'healthy' else 1)

    # Standardize features
    scaler = StandardScaler()
    data[['points_per_game', 'assists_per_game', 'rebounds_per_game', 'win_rate', 'player_fatigue']] = scaler.fit_transform(
        data[['points_per_game', 'assists_per_game', 'rebounds_per_game', 'win_rate', 'player_fatigue']])

    return data

def main():
    data = load_data()
    data = create_features(data)
    # Save or return the processed data for model training
    data.to_csv('processed_sports_data.csv', index=False)

if __name__ == "__main__":
    main()
