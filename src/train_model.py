import pandas as pd
import joblib
import os
from itertools import combinations
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import numpy as np

# Paths
DATA_PATH = os.path.join("..", "Data", "team_2025.csv")
MODEL_PATH = os.path.join("..", "models", "model.pkl")

# Load team data
teams = pd.read_csv(DATA_PATH)


def create_training_data(teams):
    X = []
    y = []

    # Convert to numeric and impute
    numeric_cols = ['ORating', 'DRating', 'Rank', 'ORank', 'DRank']
    teams[numeric_cols] = teams[numeric_cols].apply(pd.to_numeric, errors='coerce')
    imputer = SimpleImputer(strategy='mean')
    teams[numeric_cols] = imputer.fit_transform(teams[numeric_cols])

    # Create all possible matchups (not just sequential)
    for team1, team2 in combinations(teams.iterrows(), 2):
        team1 = team1[1]
        team2 = team2[1]

        # More comprehensive features
        features = [
            team1['ORating'] - team2['ORating'],  # Offensive difference
            team2['DRating'] - team1['DRating'],  # Defensive advantage (higher is better)
            np.log(team1['Rank']) - np.log(team2['Rank']),  # Log rank difference
            (team1['ORank'] - team2['ORank']) / 100,  # Offensive rank difference
            (team1['DRank'] - team2['DRank']) / 100,  # Defensive rank difference
            int(team1['TrapOfEx'] == 'Yes') - int(team2['TrapOfEx'] == 'Yes'),
            int(team1['KenPomTop'] == 'Yes') - int(team2['KenPomTop'] == 'Yes')
        ]

        X.append(features)
        # Use a probabilistic target based on rank difference
        # This gives more nuance than just 1/0
        prob = 1 / (1 + np.exp((team1['Rank'] - team2['Rank']) / 5))
        y.append(1 if np.random.random() < prob else 0)

    return pd.DataFrame(X, columns=[
        'ORating_Diff',
        'DRating_Advantage',
        'LogRank_Diff',
        'ORank_Diff',
        'DRank_Diff',
        'TrapOfEx_Advantage',
        'KenPomTop_Advantage'
    ]), np.array(y)


# Create dataset
X, y = create_training_data(teams)

# Scale features
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Use Random Forest for better probability calibration
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model and scaler
joblib.dump({'model': model, 'scaler': scaler}, MODEL_PATH)
print(f"✅ Model trained and saved to {MODEL_PATH}")