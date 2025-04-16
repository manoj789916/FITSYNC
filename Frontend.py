import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64

# Set Streamlit page config
st.set_page_config(page_title="Personal Fitness Tracker", layout="centered")

# Function to encode local image to Base64
def get_base64_image(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Add background image using encoded Base64 image
def set_bg(img_path):
    img_base64 = get_base64_image(img_path)
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{img_base64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Set your background
set_bg("C:/Users/Shalini/Downloads/bg.jpeg")  # Adjust path if needed

# Title
st.title("🏋️ FitSynq Tracker AI")
st.markdown("""
Track your workouts and estimate calories burned based on your personal details and heart rate.
""")

# Sidebar for personal information
st.sidebar.header("User Information")
age = st.sidebar.number_input("Age", min_value=1, max_value=120, value=25)
height = st.sidebar.number_input("Height (cm)", min_value=50, max_value=250, value=170)
weight = st.sidebar.number_input("Weight (kg)", min_value=20, max_value=300, value=70)
gender = st.sidebar.radio("Gender", ["Male", "Female"])

# Exercise selection
st.header("🏃‍♀️ Workout Details")
exercise = st.selectbox("Select Exercise", ["Walking", "Running", "Swimming", "Cycling"])
duration = st.slider("Duration (minutes)", 1, 180, 30)
heart_rate = st.number_input("Average Heart Rate during Exercise (bpm)", min_value=60, max_value=200, value=120)

# MET values for different exercises
met_values = {
    "Walking": 3.5,
    "Running": 7.0,
    "Swimming": 8.0,
    "Cycling": 6.8
}

# Calculate calories burned
def calculate_calories(met, weight_kg, duration_min):
    return met * weight_kg * (duration_min / 60)

met = met_values[exercise]
calories_burned = calculate_calories(met, weight, duration)

# Display results
st.subheader("🏋️ Results")
st.markdown(f"**Calories Burned:** {calories_burned:.2f} kcal")
st.markdown(f"**Heart Rate:** {heart_rate} bpm")

# Heart rate zone
st.subheader("📈 Heart Rate Zone")
max_hr = 220 - age
hr_percent = (heart_rate / max_hr) * 100

if hr_percent < 50:
    zone = "Very Light - Good for recovery"
elif hr_percent < 60:
    zone = "Light - Improves basic endurance"
elif hr_percent < 70:
    zone = "Moderate - Improves aerobic fitness"
elif hr_percent < 80:
    zone = "Hard - Improves performance"
else:
    zone = "Maximum - Only for short bursts"

st.markdown(f"**You are in the:** {zone} zone")

# Visualization
st.subheader("🌍 Visualization")
data = pd.DataFrame({
    'Category': ['Calories Burned', 'Max Heart Rate', 'Current Heart Rate'],
    'Value': [calories_burned, max_hr, heart_rate]
})

fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(x='Category', y='Value', data=data, palette='coolwarm', ax=ax)
ax.set_title('Workout Summary')
st.pyplot(fig)

