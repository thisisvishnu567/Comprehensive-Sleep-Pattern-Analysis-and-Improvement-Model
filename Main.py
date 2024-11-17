import streamlit as st
import pandas as pd
import os
import joblib
import numpy as np

# Load the trained model
model_path = "sleep_quality_model.pkl"
if os.path.exists(model_path):
    sleep_quality_model = joblib.load(model_path)
else:
    st.error("Trained model not found! Please run `train_model.py` to train the model first.")
    sleep_quality_model = None

# Path to user data CSV
user_data_path = "userdata.csv"

# Function to predict sleep quality
def predict_sleep_quality(inputs):
    input_data = np.array([[
        inputs["Age"],
        inputs["Daily Steps"],
        inputs["Calories Burned"],
        1 if inputs["Physical Activity Level"] == "low" else 2 if inputs["Physical Activity Level"] == "medium" else 3,
        1 if inputs["Dietary Habits"] == "unhealthy" else 2 if inputs["Dietary Habits"] == "medium" else 3,
        1 if inputs["Sleep Disorders"] == "yes" else 0,
        1 if inputs["Medication Usage"] == "yes" else 0,
    ]])
    return sleep_quality_model.predict(input_data)[0]

# Function to load user data
def load_user_data():
    if os.path.exists(user_data_path):
        return pd.read_csv(user_data_path)
    else:
        return pd.DataFrame(columns=["Name", "Age", "Daily Steps", "Calories Burned", 
                                     "Physical Activity Level", "Dietary Habits", 
                                     "Sleep Disorders", "Medication Usage", "Sleep Quality"])

# Function to save user data
def save_user_data(data):
    df = pd.DataFrame([data])
    if os.path.exists(user_data_path):
        df.to_csv(user_data_path, mode='a', header=False, index=False)
    else:
        df.to_csv(user_data_path, index=False)

# Initialize session state
if "user_data" not in st.session_state:
    st.session_state.user_data = {}

st.title("Sleep Analyser")

# Form for user details
with st.form("user_details_form"):
    st.header("Enter Sleep Details")
    name = st.text_input("Name:", value=st.session_state.user_data.get('Name', ''))
    age = st.number_input("Age:", min_value=0, max_value=120, value=st.session_state.user_data.get('Age', 0))
    daily_steps = st.number_input("Daily Steps:", min_value=0, value=st.session_state.user_data.get('Daily Steps', 0))
    calories_burned = st.number_input("Calories Burned per day:", min_value=0, value=st.session_state.user_data.get('Calories Burned', 0))
    physical_activity_level = st.selectbox("Physical Activity Level:", ["low", "medium", "high"], index=0)
    dietary_habits = st.selectbox("Dietary Habits:", ["healthy", "medium", "unhealthy"], index=0)
    sleep_disorders = st.selectbox("Sleep Disorders:", ["yes", "no"], index=1)
    medication_usage = st.selectbox("Medication Usage:", ["yes", "no"], index=1)

    # Save user input
    submit_button = st.form_submit_button("Save and Predict")

    if submit_button:
        st.session_state.user_data = {
            "Name": name,
            "Age": age,
            "Daily Steps": daily_steps,
            "Calories Burned": calories_burned,
            "Physical Activity Level": physical_activity_level,
            "Dietary Habits": dietary_habits,
            "Sleep Disorders": sleep_disorders,
            "Medication Usage": medication_usage,
        }
        # Predict sleep quality
        predicted_quality = predict_sleep_quality(st.session_state.user_data)
        st.session_state.user_data["Sleep Quality"] = round(predicted_quality, 2)
        save_user_data(st.session_state.user_data)
        st.success(f"Predicted Sleep Quality: {predicted_quality:.2f}/10")

# Display past user data
st.header("Previous Records")
user_data = load_user_data()
st.write(user_data)
