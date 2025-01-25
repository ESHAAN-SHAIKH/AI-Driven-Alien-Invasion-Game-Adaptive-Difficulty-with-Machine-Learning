import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

# Load the data
df = pd.read_csv('player_metrics.csv')

# Drop rows with missing values
df.dropna(inplace=True)

# Ensure these columns exist in your DataFrame
if all(col in df.columns for col in ['reaction_time', 'accuracy', 'lives_lost', 'alien_speed']):
    X = df[['reaction_time', 'accuracy', 'lives_lost']]  # Features
    y = df['alien_speed']  # Target variable

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model = RandomForestRegressor()
    model.fit(X_train, y_train)

    # Save the model
    joblib.dump(model, 'difficulty_model.pkl')
else:
    print("Required columns are missing from the CSV file.")

