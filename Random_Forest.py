import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib

# Step 1: Load the Dataset (Replace with real data)
# Create a dummy dataset for training (or use a real dataset)
data = pd.DataFrame({
    "Age": [20, 25, 30, 35, 40, 45, 50, 55],
    "Daily Steps": [3000, 7000, 10000, 4000, 5000, 8000, 6000, 2000],
    "Calories Burned": [1500, 2000, 2200, 1800, 1900, 2100, 1700, 1400],
    "Physical Activity Level": [1, 3, 2, 1, 2, 3, 2, 1],  # Encoded: low=1, medium=2, high=3
    "Dietary Habits": [1, 3, 2, 2, 1, 3, 2, 1],           # Encoded: healthy=3, medium=2, unhealthy=1
    "Sleep Disorders": [0, 0, 1, 0, 1, 0, 1, 0],          # Encoded: no=0, yes=1
    "Medication Usage": [0, 1, 0, 0, 1, 0, 1, 0],         # Encoded: no=0, yes=1
    "Sleep Quality": [7, 9, 6, 5, 6, 8, 7, 4]             # Target variable
})

# Step 2: Split Data into Features and Target
X = data.drop("Sleep Quality", axis=1)  # Features
y = data["Sleep Quality"]  # Target (sleep quality)

# Step 3: Split into Train/Test Sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Train the Random Forest Model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Step 5: Evaluate the Model
predictions = model.predict(X_test)
print("Mean Squared Error:", mean_squared_error(y_test, predictions))

# Step 6: Save the Trained Model to a File
joblib.dump(model, "sleep_quality_model.pkl")
print("Model saved as 'sleep_quality_model.pkl'")
