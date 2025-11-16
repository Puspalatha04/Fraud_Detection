
import streamlit as st
import pandas as pd
import joblib
# Import database functions from utils.py
from utils import get_db_connection, initialize_database, create_user, authenticate_user, reset_user_password

# --- Database Initialization (should only be called once in app.py) ---
if 'db_initialized' not in st.session_state:
    initialize_database()
    st.session_state.db_initialized = True

# --- Model and Scaler Loading (existing functions) ---
@st.cache_resource
def load_model_and_scaler():
    model = joblib.load('./random_forest_model.joblib')
    scaler = joblib.load('./scaler.joblib')
    return model, scaler

model, scaler = load_model_and_scaler()

# --- Preprocessing Column Definitions (existing definitions) ---
categorical_cols_for_ohe = [
    'Transaction_Location',
    'Card_Type',
    'Transaction_Currency',
    'Transaction_Status',
    'Authentication_Method',
    'Transaction_Category'
]

numerical_cols_to_scale = [
    'Transaction_Amount',
    'Previous_Transaction_Count',
    'Distance_Between_Transactions_km',
    'Time_Since_Last_Transaction_min',
    'Transaction_Velocity'
]

final_model_features = [
    'Transaction_Amount', 'Previous_Transaction_Count', 'Distance_Between_Transactions_km',
    'Time_Since_Last_Transaction_min', 'Transaction_Velocity', 'Transaction_Hour',
    'Transaction_DayOfWeek', 'Transaction_Month',
    'Transaction_Location_Bukhara', 'Transaction_Location_Fergana', 'Transaction_Location_Jizzakh',
    'Transaction_Location_Kashkadarya', 'Transaction_Location_Khorezm', 'Transaction_Location_Namangan',
    'Transaction_Location_Navoiy', 'Transaction_Location_Samarkand', 'Transaction_Location_Sirdarya',
    'Transaction_Location_Surkhandarya', 'Transaction_Location_Tashkent',
    'Card_Type_UzCard', 'Transaction_Currency_UZS',
    'Transaction_Status_Reversed', 'Transaction_Status_Successful',
    'Authentication_Method_Biometric', 'Authentication_Method_Password',
    'Transaction_Category_Cash Out', 'Transaction_Category_Payment', 'Transaction_Category_Transfer'
]

# --- Prediction Function (existing function) ---
def predict_transaction(raw_input_data):
    df_single = pd.DataFrame([raw_input_data])

    # 1. Date/Time Feature Engineering
    df_single['Transaction_DateTime'] = pd.to_datetime(df_single['Transaction_Date'] + ' ' + df_single['Transaction_Time'], format='%m/%d/%Y %H:%M')
    df_single['Transaction_Hour'] = df_single['Transaction_DateTime'].dt.hour
    df_single['Transaction_DayOfWeek'] = df_single['Transaction_DateTime'].dt.dayofweek
    df_single['Transaction_Month'] = df_single['Transaction_DateTime'].dt.month
    df_single = df_single.drop(columns=['Transaction_Date', 'Transaction_Time', 'Transaction_DateTime'])

    # 2. One-Hot Encoding
    df_single = pd.get_dummies(df_single, columns=categorical_cols_for_ohe, drop_first=True)

    # 3. Align columns with the training data (X_train)
    df_single = df_single.reindex(columns=final_model_features, fill_value=0)

    # 4. Scale numerical features
    df_single[numerical_cols_to_scale] = scaler.transform(df_single[numerical_cols_to_scale])

    # Make prediction
    prediction = model.predict(df_single)[0]
    prob = model.predict_proba(df_single)[0][1]

    return "Fraud" if prediction == 1 else "Legit", round(prob, 4)

# --- Streamlit App Interface - Overview Page ---
st.set_page_config(page_title="Fraud Detection App", layout="wide")

# Initialize session state for login status
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.user_id = None

def show_login_form():
    st.sidebar.subheader("Login")
    with st.sidebar.form("login_form"): # Added key to form
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        login_button = st.form_submit_button("Login")

        if login_button:
            user = authenticate_user(username, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.username = user['username']
                st.session_state.user_id = user['id']
                st.sidebar.success(f"Logged in as {st.session_state.username}")
                st.rerun()
            else:
                st.sidebar.error("Invalid username or password")

def show_register_form():
    st.sidebar.subheader("Register")
    with st.sidebar.form("register_form", clear_on_submit=True): # Added key and clear_on_submit
        new_username = st.text_input("New Username", key="register_new_username")
        new_password = st.text_input("New Password", type="password", key="register_new_password")
        register_button = st.form_submit_button("Register")

        if register_button:
            if new_username and new_password:
                if create_user(new_username, new_password):
                    st.sidebar.success(f"Registration successful for {new_username}. Please log in.")
                    # Explicitly clear inputs by resetting session state keys, if clear_on_submit doesn't work
                    if "register_new_username" in st.session_state: del st.session_state["register_new_username"]
                    if "register_new_password" in st.session_state: del st.session_state["register_new_password"]
                    st.rerun()
                # Error message already handled by create_user
            else:
                st.sidebar.error("Username and password cannot be empty.")

def show_logout_button():
    if st.sidebar.button("Logout"): # Added key to button
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.user_id = None
        st.info("Logged out successfully.")
        st.rerun()

# --- Main App Logic ---
# Display sidebar content based on login status
if st.session_state.logged_in:
    st.sidebar.write(f"Welcome, {st.session_state.username}!")
    show_logout_button()
    # Add a link to reset password for logged-in users too
    st.sidebar.page_link("pages/4_Reset_Password.py", label="Reset Password", icon="🔒")
else:
    st.title("Welcome! Please Login or Register to continue.")
    show_login_form()
    show_register_form()
    st.info("You need to log in to access the fraud detection features.")
    st.sidebar.page_link("pages/4_Reset_Password.py", label="Reset Password", icon="🔒") # Accessible when logged out

# Only display app overview if logged in, otherwise the login/register message takes precedence
if st.session_state.logged_in:
    st.title("App Overview 💳 Welcome to the Real-time Transaction Fraud Detection System")

    st.markdown("""
    This application leverages machine learning to identify potentially fraudulent financial transactions in real-time.
    Using a trained Random Forest Classifier, it assesses various transaction attributes to predict the likelihood of fraud.

    ### How it works:

    1.  **Data Preprocessing**: Raw transaction data is transformed, including date/time feature engineering, one-hot encoding for categorical variables, and scaling of numerical features.
    2.  **Model Prediction**: The preprocessed data is fed into a Random Forest model, which outputs a prediction (Fraud/Legit) and a probability score.

    Navigate to the 'Fraud Prediction' page to test a single transaction or to other potential pages for analytics or batch processing.
    """)
