import joblib
import os
import pandas as pd
import numpy as np

# Paths
MODEL_PATH = os.path.join("..", "models", "model.pkl")
DATA_PATH = os.path.join("..", "Data", "team_2025.csv")

# Load model and data
model_data = joblib.load(MODEL_PATH)
model = model_data['model']
scaler = model_data['scaler']
teams = pd.read_csv(DATA_PATH)


def get_team_data(team_name):
    team_data = teams[teams["Name"].str.lower() == team_name.lower()]
    if team_data.empty:
        return None

    team = team_data.iloc[0].copy()

    # Convert numeric columns
    numeric_cols = ['ORating', 'DRating', 'Rank', 'ORank', 'DRank']
    for col in numeric_cols:
        team[col] = pd.to_numeric(team[col], errors='coerce')

    return team


def predict_winner(team_name_1, team_name_2):
    team_1 = get_team_data(team_name_1)
    team_2 = get_team_data(team_name_2)

    if team_1 is None or team_2 is None:
        print("❌ One or both team names are invalid.")
        return None

    # Prepare features
    features = [
        float(team_1['ORating']) - float(team_2['ORating']),
        float(team_2['DRating']) - float(team_1['DRating']),  # Note this is inverted for advantage
        np.log(float(team_1['Rank'])) - np.log(float(team_2['Rank'])),
        (float(team_1['ORank']) - float(team_2['ORank'])) / 100,
        (float(team_1['DRank']) - float(team_2['DRank'])) / 100,
        int(team_1['TrapOfEx'] == 'Yes') - int(team_2['TrapOfEx'] == 'Yes'),
        int(team_1['KenPomTop'] == 'Yes') - int(team_2['KenPomTop'] == 'Yes')
    ]

    # Scale features
    features_scaled = scaler.transform([features])

    # Get probabilities
    prob_team1 = model.predict_proba(features_scaled)[0][1]
    prob_team2 = 1 - prob_team1

    # Apply softmax to ensure reasonable probabilities for close matchups
    def softmax(x):
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum()

    probs = softmax([prob_team1, prob_team2])
    prob_team1, prob_team2 = probs[0], probs[1]

    print("\n📊 Prediction Results:")
    print(f"{team_name_1}: {prob_team1 * 100:.1f}% chance to win")
    print(f"{team_name_2}: {prob_team2 * 100:.1f}% chance to win")

    # Determine confidence level
    diff = abs(prob_team1 - prob_team2)
    if diff < 0.1:
        confidence = "⚠️ Toss-up - Essentially a coin flip"
    elif diff < 0.2:
        confidence = "🔍 Slight edge"
    elif diff < 0.3:
        confidence = "📈 Moderate confidence"
    else:
        confidence = "✅ High confidence"

    print(f"\n{confidence} in this prediction")

    winner = team_name_1 if prob_team1 > prob_team2 else team_name_2
    print(f"\n🏆 Predicted Winner: {winner}")

    # Key factors analysis
    print("\n🔑 Key Factors:")
    factors = []

    # Offensive comparison
    orating_diff = float(team_1['ORating']) - float(team_2['ORating'])
    if abs(orating_diff) > 2:
        factors.append(
            f"{team_name_1 if orating_diff > 0 else team_name_2} has significantly better offense (+{abs(orating_diff):.1f})")

    # Defensive comparison
    drating_diff = float(team_2['DRating']) - float(team_1['DRating'])  # Lower DRating is better
    if abs(drating_diff) > 2:
        factors.append(
            f"{team_name_1 if drating_diff > 0 else team_name_2} has better defense ({min(float(team_1['DRating']), float(team_2['DRating'])):.1f} vs {max(float(team_1['DRating']), float(team_2['DRating'])):.1f})")

    # Rank comparison
    rank_diff = float(team_1['Rank']) - float(team_2['Rank'])
    if abs(rank_diff) >= 5:
        factors.append(
            f"{team_name_1 if rank_diff < 0 else team_name_2} is significantly higher ranked (#{int(min(float(team_1['Rank']), float(team_2['Rank'])))} vs #{int(max(float(team_1['Rank']), float(team_2['Rank'])))})")

    # Special factors
    if team_1['TrapOfEx'] == 'Yes' and team_2['TrapOfEx'] != 'Yes':
        factors.append(f"{team_name_1} has Tournament Experience advantage")
    elif team_2['TrapOfEx'] == 'Yes' and team_1['TrapOfEx'] != 'Yes':
        factors.append(f"{team_name_2} has Tournament Experience advantage")

    if not factors:
        print("- The teams are very evenly matched on key metrics")
    else:
        # Show top 3 factors
        for factor in factors[:3]:  
            print(f"- {factor}")

    # Style matchup
    print("\n🎯 Style Matchup:")
    styles = []
    if float(team_1['ORating']) > 125 and float(team_2['ORating']) > 125:
        styles.append("Both teams have elite offenses - expect high scoring")
    if float(team_1['DRating']) < 90 and float(team_2['DRating']) < 90:
        styles.append("Both teams play strong defense - lower scoring likely")
    if (float(team_1['ORating']) > 125 and float(team_2['DRating']) < 90) or (
            float(team_2['ORating']) > 125 and float(team_1['DRating']) < 90):
        styles.append("Classic offense vs defense matchup")

    print("\n".join(styles) if styles else "No dominant style advantages")


if __name__ == "__main__":
    team_1 = input("Enter the name of Team 1: ")
    team_2 = input("Enter the name of Team 2: ")
    predict_winner(team_1, team_2)