import streamlit as st
import pickle
import pandas as pd
from model import load_and_process_data, predict_disease
from utils import authenticate_user, create_user
import random

# Load preprocessed data
nutrition_data = load_and_process_data()

# Authentication and Registration Pages
def login_page():
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if authenticate_user(username, password):
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success("Login successful!")
            user_homepage()  # Redirect to the homepage after login
        else:
            st.error("Invalid credentials. Please try again.")

def register_page():
    st.title("Register Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    
    if st.button("Register"):
        if password == confirm_password:
            create_user(username, password)
            st.success("Registration successful! Please log in.")
        else:
            st.error("Passwords do not match.")

# User Homepage with input form for meal plan generation
def user_homepage():
    # Check if user is logged in
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.warning("Please log in to access the meal plan.")
        return
    
    st.title(f"Welcome, {st.session_state['username']}!")
    
    # User info form for dietary preferences and health conditions
    with st.form("dietary_form"):
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=18, max_value=100)
        weight = st.number_input("Weight (kg)", min_value=30.0, max_value=150.0)
        height = st.number_input("Height (cm)", min_value=120, max_value=250)
        dietary_pref = st.selectbox("Dietary Preference", nutrition_data['Dietary Preference'].unique())
        
        health_conditions = st.multiselect("Health Conditions", ["Weight Loss", "Kidney Disease", "Weight Gain", "Hypertension", "Diabetes", "Acne", "Heart Disease"])
        
        submit_button = st.form_submit_button("Generate Meal Plan")
        
        if submit_button:
            recommend_meals(name, age, weight, height, dietary_pref, health_conditions)

# Meal recommendations based on user input
def recommend_meals(name, age, weight, height, dietary_pref, health_conditions):
    # Filtering data based on dietary preferences and health conditions
    filtered_data = nutrition_data[nutrition_data['Dietary Preference'].str.contains(dietary_pref, case=False, na=False)].copy()
    
    if health_conditions:
        health_condition_pattern = '|'.join(health_conditions)
        filtered_data = filtered_data[filtered_data['Disease'].str.contains(health_condition_pattern, case=False, na=False)]
    
    if filtered_data.empty:
        st.warning(f"Hello {name}, we couldn't find any meal plan based on your input.")
        return

    # BMI Calculation
    height_m = height / 100  # Convert cm to meters
    bmi = weight / (height_m ** 2)
    st.write(f"Your BMI is: {bmi:.2f}")
    
    # Recommend meals based on BMI
    if bmi < 18.5:
        st.warning("Your BMI is below the normal range. Consider a diet to help with weight gain.")
    elif 18.5 <= bmi < 24.9:
        st.success("Your BMI is within the normal range. Maintain a balanced diet!")
    else:
        st.warning("Your BMI is above the normal range. Consider a diet plan for weight management.")
    
    # Generate weekly meal plan
    weekly_plan = pd.DataFrame({
        "Day": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "Breakfast": [random.choice(filtered_data["Breakfast Suggestion"].dropna().tolist()) for _ in range(7)],
        "Lunch": [random.choice(filtered_data["Lunch Suggestion"].dropna().tolist()) for _ in range(7)],
        "Dinner": [random.choice(filtered_data["Dinner Suggestion"].dropna().tolist()) for _ in range(7)],
        "Snack": [random.choice(filtered_data["Snack Suggestion"].dropna().tolist()) for _ in range(7)]
    })
    
    st.write("Here’s a suggested weekly meal plan based on your preferences and health conditions:")
    st.table(weekly_plan)

# Main program logic
def main():
    # Check if the user is logged in
    if "logged_in" in st.session_state and st.session_state["logged_in"]:
        user_homepage()
    else:
        # Authentication page or registration page
        st.sidebar.title("Nutrition App")
        page = st.sidebar.radio("Choose a page", ("Login", "Register"))
        
        if page == "Login":
            login_page()
        elif page == "Register":
            register_page()

if __name__ == "__main__":
    main()
