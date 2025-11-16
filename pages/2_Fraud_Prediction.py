
import streamlit as st
import pandas as pd
import sqlite3
import json
from datetime import datetime
# Import necessary functions/objects from app.py and utils.py
from app import predict_transaction, model, scaler, categorical_cols_for_ohe, numerical_cols_to_scale, final_model_features
from utils import get_db_connection

# Set page configuration
st.set_page_config(page_title="Fraud Prediction", layout="wide")

st.title("🕵️ Real-time Fraud Prediction")
st.markdown("Input the details of a transaction below to get an instant fraud prediction.")

# Check if user is logged in
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in to make fraud predictions.")
else:
    # Interactive form for transaction details
    with st.form("fraud_prediction_form"):
        st.subheader("Enter Transaction Details")

        col1, col2, col3 = st.columns(3)
        with col1:
            transaction_amount = st.number_input("Transaction Amount (e.g., 500000)", min_value=1.0, value=500000.0, step=10000.0)
            transaction_date = st.date_input("Transaction Date", value=pd.to_datetime('today'))
            transaction_time = st.time_input("Transaction Time", value=pd.to_datetime('now').time())
            transaction_location = st.selectbox("Transaction Location", [
                'Andijan', 'Bukhara', 'Fergana', 'Jizzakh', 'Kashkadarya', 'Khorezm', 'Namangan',
                'Navoiy', 'Samarkand', 'Sirdarya', 'Surkhandarya', 'Tashkent'
            ], index=8) # Default to Samarkand for example

        with col2:
            card_type = st.selectbox("Card Type", ['Humo', 'UzCard', 'Visa'], index=0) # Default to Humo
            transaction_currency = st.selectbox("Transaction Currency", ['UZS', 'USD'], index=0) # Default to UZS
            transaction_status = st.selectbox("Transaction Status", ['Failed', 'Pending', 'Reversed', 'Successful'], index=3) # Default to Successful
            authentication_method = st.selectbox("Authentication Method", ['2FA', 'Biometric', 'Password'], index=2) # Default to Password

        with col3:
            previous_transaction_count = st.slider("Previous Transaction Count", 1, 50, 25)
            distance_between_transactions_km = st.slider("Distance Between Transactions (km)", 0.0, 5000.0, 1500.0, step=1.0)
            time_since_last_transaction_min = st.slider("Time Since Last Transaction (min)", 1, 1440, 500)
            transaction_velocity = st.slider("Transaction Velocity (transactions/hour)", 1, 10, 6)
            transaction_category = st.selectbox("Transaction Category", [
                'Cash In', 'Cash Out', 'Payment', 'Transfer'
            ], index=2) # Default to Payment

        submitted = st.form_submit_button("Predict Fraud")

        if submitted:
            # Prepare raw input data for prediction
            raw_input = {
                'Transaction_Amount': transaction_amount,
                'Transaction_Date': transaction_date.strftime('%m/%d/%Y'),
                'Transaction_Time': transaction_time.strftime('%H:%M'),
                'Transaction_Location': transaction_location,
                'Card_Type': card_type,
                'Transaction_Currency': transaction_currency,
                'Transaction_Status': transaction_status,
                'Previous_Transaction_Count': previous_transaction_count,
                'Distance_Between_Transactions_km': distance_between_transactions_km,
                'Time_Since_Last_Transaction_min': time_since_last_transaction_min,
                'Authentication_Method': authentication_method,
                'Transaction_Velocity': transaction_velocity,
                'Transaction_Category': transaction_category,
                'Merchant_ID': 0, # Placeholder, as it will be dropped by the prediction function
                'Device_ID': 0 # Placeholder, as it will be dropped by the prediction function
            }

            # Get prediction using the imported function
            status, prob = predict_transaction(raw_input)

            st.subheader("\nPrediction Result:")
            if status == "Fraud":
                st.error(f"🚨 Fraudulent Transaction Detected! Probability: {prob}")
            else:
                st.success(f"✅ Legitimate Transaction. Probability: {prob}")

            # Record the prediction in the database if user is logged in
            if st.session_state.logged_in and st.session_state.user_id:
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()

                    timestamp = datetime.now().isoformat()
                    raw_input_json = json.dumps(raw_input)

                    cursor.execute(
                        "INSERT INTO transactions (user_id, timestamp, raw_input, prediction, probability) VALUES (?, ?, ?, ?, ?)",
                        (st.session_state.user_id, timestamp, raw_input_json, status, prob)
                    )
                    conn.commit()
                    st.info("Prediction successfully recorded in your transaction history.")
                except sqlite3.Error as e:
                    st.error(f"Error recording transaction history: {e}")
                finally:
                    if conn:
                        conn.close()
            else:
                st.warning("Log in to record your prediction in the transaction history.")
