
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io

# Set page configuration
st.set_page_config(page_title="Dataset Information and EDA", layout="wide")

st.title("📊 Dataset Information and Exploratory Data Analysis (EDA)")
st.markdown("This page provides an overview of the dataset structure, statistics, and distributions of key features.")

# Check if user is logged in
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in to view dataset information and EDA.")
else:
    # Load the dataset
    @st.cache_data
    def load_data():
        df = pd.read_csv('./card_fraud.csv')
        return df

    df = load_data()

    st.subheader("Dataset Overview")
    st.write(f"DataFrame has {df.shape[0]} rows and {df.shape[1]} columns.")

    st.subheader("DataFrame Info (Column Details):")

    # Create a DataFrame for df.info() details for better formatting
    info_data = []
    for col in df.columns:
        info_data.append({
            'Column Name': col,
            'Data Type': df[col].dtype,
            'Non-Null Count': df[col].count(),
            'Null Count': df[col].isnull().sum(),
            'Unique Values': df[col].nunique() # Added for categorical insights
        })
    info_df = pd.DataFrame(info_data)
    st.dataframe(info_df)

    st.subheader("Descriptive Statistics:")
    st.dataframe(df.describe())

    # Numerical Features Distribution
    numerical_cols = [
        'Transaction_Amount',
        'Previous_Transaction_Count',
        'Distance_Between_Transactions_km',
        'Time_Since_Last_Transaction_min',
        'Transaction_Velocity'
    ]

    st.subheader("Distribution of Numerical Features")
    for col in numerical_cols:
        st.markdown(f"#### {col}")
        fig, axes = plt.subplots(1, 2, figsize=(15, 5))

        # Histogram
        sns.histplot(df[col], kde=True, ax=axes[0])
        axes[0].set_title(f'Histogram of {col}')
        axes[0].set_xlabel(col)
        axes[0].set_ylabel('Frequency')

        # Box plot
        sns.boxplot(x=df[col], ax=axes[1])
        axes[1].set_title(f'Box Plot of {col}')
        axes[1].set_xlabel(col)

        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    # Categorical Features Distribution
    categorical_cols_to_plot = [
        'Transaction_Location',
        'Card_Type',
        'Transaction_Currency',
        'Transaction_Status',
        'Authentication_Method',
        'Transaction_Category'
    ]

    st.subheader("Distribution of Categorical Features")
    for col in categorical_cols_to_plot:
        st.markdown(f"#### {col}")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.countplot(data=df, x=col, hue=col, palette='viridis', legend=False, ax=ax)
        ax.set_title(f'Distribution of {col}')
        ax.set_xlabel(col)
        ax.set_ylabel('Count')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    # Target Variable Distribution
    st.subheader("Distribution of Target Variable ('isFraud')")
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.countplot(data=df, x='isFraud', palette='coolwarm', ax=ax)
    ax.set_title('Distribution of isFraud Target Variable')
    ax.set_xlabel('Is Fraudulent Transaction')
    ax.set_ylabel('Count')
    ax.set_xticks(ticks=[0, 1], labels=['Not Fraud (0)', 'Fraud (1)'])
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.success("Dataset Information and EDA page loaded successfully!")
