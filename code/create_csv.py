import pandas as pd

# Create a dictionary with some sample data
data = {
    'reaction_time': [0.5, 1.0, 1.5],
    'accuracy': [0.75, 0.80, 0.60],
    'lives_lost': [1, 0, 2],
    'alien_speed': [1.0, 1.5, 2.0]  # Example target variable
}

# Create a DataFrame from the dictionary
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv('player_metrics.csv', index=False)

print("CSV file created successfully.")
