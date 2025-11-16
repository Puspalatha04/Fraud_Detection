
import streamlit as st
import pandas as pd
import sqlite3
import json
from datetime import datetime
import io

# Import necessary functions/objects from utils.py
from utils import get_db_connection

# Set page configuration
st.set_page_config(page_title="User Transaction History", layout="wide")

st.title("📜 Your Transaction History")
st.markdown("View and download your past transaction predictions.")

# Check if user is logged in
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in to view your transaction history.")
else:
    user_id = st.session_state.user_id
    st.write(f"Welcome, {st.session_state.username}! Here are your recorded transactions:")

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT timestamp, raw_input, prediction, probability FROM transactions WHERE user_id = ? ORDER BY timestamp DESC",
            (user_id,)
        )
        records = cursor.fetchall()

        if records:
            # Convert records to a list of dictionaries for easier DataFrame creation
            transaction_data = []
            for record in records:
                row_dict = dict(record)
                raw_input_dict = json.loads(row_dict['raw_input'])
                # Merge raw_input details with other record details
                transaction_data.append({
                    'Timestamp': row_dict['timestamp'],
                    'Prediction': row_dict['prediction'],
                    'Probability': row_dict['probability'],
                    **raw_input_dict # Expand raw_input dictionary into individual columns
                })

            df_history = pd.DataFrame(transaction_data)

            # Reorder columns for better readability, putting prediction first
            cols = ['Timestamp', 'Prediction', 'Probability'] + \
                   [col for col in df_history.columns if col not in ['Timestamp', 'Prediction', 'Probability']]
            df_history = df_history[cols]

            st.subheader("Transaction List")
            st.dataframe(df_history)

            # --- Excel Export Functionality ---
            def to_excel(df):
                output = io.BytesIO()
                writer = pd.ExcelWriter(output, engine='xlsxwriter')
                df.to_excel(writer, index=False, sheet_name='Transaction History')
                writer.close()
                processed_data = output.getvalue()
                return processed_data

            st.download_button(
                label="Download History as Excel",
                data=to_excel(df_history),
                file_name=f"transaction_history_{st.session_state.username}_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.info("No transaction history found for your account.")

    except sqlite3.Error as e:
        st.error(f"Error fetching transaction history: {e}")
    finally:
        if conn:
            conn.close()
