import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
df = pd.read_csv("indian_weather_data.csv")

# -----------------------------
# Create Proxy Label (IMPORTANT)
# -----------------------------
# Example rule: high temp + dry weather = wildfire risk
df['risk'] = ((df['Temperature'] > 35) & (df['weather_code'] < 120)).astype(int)

# Features & Target
X = df[['wind_speed', 'humidity', 'Temperature']]
y = df['risk']

# Train model
model = RandomForestClassifier()
model.fit(X, y)

# Save model
joblib.dump(model, "model.pkl")

print("✅ Model saved as model.pkl")