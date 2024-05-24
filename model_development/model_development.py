import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import sqlite3
import numpy as np

def fetch_data_from_db(query):
    conn = sqlite3.connect('sports_data.db')
    data = pd.read_sql_query(query, conn)
    conn.close()
    return data

def prepare_data():
    query = """
    SELECT 
        ps.player_id, ps.points_per_game, ps.assists_per_game, ps.rebounds_per_game, 
        ts.win_rate, i.injury_status, o.home_team_odds, o.away_team_odds
    FROM PlayerStats ps
    JOIN TeamStats ts ON ps.team = ts.team_name
    LEFT JOIN injuries i ON ps.player_id = i.player_id
    JOIN odds o ON ps.team = o.home_team OR ps.team = o.away_team
    WHERE ps.season = 2023 AND ts.season = 2023
    """
    data = fetch_data_from_db(query)
    data = data.fillna({'injury_status': 'Healthy'})
    data['injury_status'] = data['injury_status'].apply(lambda x: 0 if x == 'Healthy' else 1)
    return data

def train_model(data):
    X = data[['points_per_game', 'assists_per_game', 'rebounds_per_game', 'win_rate', 'injury_status']]
    y = (data['home_team_odds'] < 0).astype(int)  # Binary target for classification
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Confusion Matrix:
", confusion_matrix(y_test, y_pred))
    print("Classification Report:
", classification_report(y_test, y_pred))
    
    return model

def calculate_kelly_criterion(probability, odds):
    # Kelly Criterion formula: f* = (bp - q) / b
    # b = odds - 1, p = probability, q = 1 - p
    b = odds - 1
    q = 1 - probability
    kelly_fraction = (probability * b - q) / b
    return kelly_fraction

def find_arbitrage_opportunities(odds_list):
    opportunities = []
    for odds in odds_list:
        implied_prob_home = calculate_implied_probabilities(odds['home_team_odds'])
        implied_prob_away = calculate_implied_probabilities(odds['away_team_odds'])
        if implied_prob_home + implied_prob_away < 1:
            opportunities.append(odds)
    return opportunities

def main():
    data = prepare_data()
    model = train_model(data)
    
    # Example probabilities for testing
    probability = 0.6
    odds = -150
    kelly_fraction = calculate_kelly_criterion(probability, odds)
    print(f"Kelly Fraction for probability {probability} and odds {odds}: {kelly_fraction}")
    
    # Example odds list for testing arbitrage opportunities
    odds_list = [{'home_team_odds': -110, 'away_team_odds': 105}]
    arbitrage_opportunities = find_arbitrage_opportunities(odds_list)
    print("Arbitrage Opportunities:", arbitrage_opportunities)

if __name__ == "__main__":
    main()


# Improvements


# Model Development Improvements

# Model Selection and Comparison
# - Experiment with other machine learning models like gradient boosting, neural networks, and ensemble methods.
# - Implement automated hyperparameter tuning (e.g., using GridSearchCV or RandomizedSearchCV) to optimize model performance.
# - Use tools like SHAP or LIME to enhance model interpretability and provide better explanations for predictions.

import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import shap

def load_data():
    # Load the processed data
    data = pd.read_csv('processed_sports_data.csv')
    return data

def prepare_data():
    data = load_data()
    X = data[['points_per_game', 'assists_per_game', 'rebounds_per_game', 'win_rate', 'injury_status', 'player_fatigue']]
    y = (data['home_team_odds'] < 0).astype(int)  # Binary target for classification
    return X, y

def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Experiment with different models
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    gb_model = GradientBoostingClassifier(n_estimators=100, random_state=42)

    models = {'Random Forest': rf_model, 'Gradient Boosting': gb_model}
    
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        print(f"{name} Model")
        print("Accuracy:", accuracy_score(y_test, y_pred))
        print("Confusion Matrix:
", confusion_matrix(y_test, y_pred))
        print("Classification Report:
", classification_report(y_test, y_pred))

        # Model interpretability with SHAP
        explainer = shap.Explainer(model, X_train)
        shap_values = explainer(X_test)
        shap.summary_plot(shap_values, X_test, plot_type="bar")

def main():
    X, y = prepare_data()
    train_model(X, y)

if __name__ == "__main__":
    main()
