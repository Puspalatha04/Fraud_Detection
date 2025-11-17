# 💳 Real-time Transaction Fraud Detection System

A machine learning-powered web application built with Streamlit for detecting fraudulent financial transactions in real-time. The system uses a Random Forest Classifier trained on 100,000 transaction records from Uzbekistan's payment ecosystem.

## 📋 Table of Contents

- [Features](#features)
- [Dataset Overview](#dataset-overview)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Model Details](#model-details)
- [Database Schema](#database-schema)
- [Screenshots](#screenshots)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- **Real-time Fraud Detection**: Instant prediction of fraudulent transactions with probability scores
- **User Authentication**: Secure login/register system with password hashing
- **Transaction History**: Track and export your prediction history to Excel
- **Interactive EDA**: Explore dataset statistics and visualizations
- **Multi-page Interface**: Clean, organized navigation across different functionalities
- **Password Reset**: Self-service password recovery
- **SQLite Database**: Persistent storage for users and transaction records

## 📊 Dataset Overview

The dataset contains **100,000 transactions** with the following features:

### Transaction Features
- **Transaction_ID**: Unique identifier for each transaction
- **User_ID**: Unique user identifier
- **Transaction_Amount**: Amount in local currency (UZS) or USD
- **Transaction_Date & Time**: Timestamp of the transaction
- **Transaction_Location**: 12 regions in Uzbekistan (Tashkent, Samarkand, Bukhara, etc.)
- **Merchant_ID**: Merchant identifier
- **Device_ID**: Device used for transaction

### Card & Payment Features
- **Card_Type**: Humo, UzCard, or Visa
- **Transaction_Currency**: UZS or USD
- **Transaction_Status**: Successful, Failed, Reversed, or Pending
- **Authentication_Method**: 2FA, Biometric, or Password

### Behavioral Features
- **Previous_Transaction_Count**: Number of previous transactions (1-50)
- **Distance_Between_Transactions_km**: Geographic distance from last transaction (0-5000 km)
- **Time_Since_Last_Transaction_min**: Time elapsed since last transaction (1-1440 min)
- **Transaction_Velocity**: Transactions per hour (1-10)
- **Transaction_Category**: Cash In, Cash Out, Payment, or Transfer

### Target Variable
- **isFraud**: Binary label (0 = Legitimate, 1 = Fraudulent)

## 📁 Project Structure

```
fraud-detection-system/
│
├── app.py                          # Main Streamlit application
├── utils.py                        # Database utility functions
├── CardFraud.ipynb                 # Jupyter notebook for model training
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
│
├── card_fraud.csv                  # Training dataset
├── random_forest_model.joblib      # Trained ML model
├── scaler.joblib                   # Feature scaler
├── app_data.db                     # SQLite database (auto-generated)
│
└── pages/                          # Streamlit multi-page app
    ├── 1_Dataset_Information_and_EDA.py
    ├── 2_Fraud_Prediction.py
    ├── 3_User_History.py
    └── 4_Reset_Password.py
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd Fraud_Detection
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Verify Required Files
Ensure these files are present:
- `card_fraud.csv` - Training dataset
- `random_forest_model.joblib` - Pre-trained model
- `scaler.joblib` - Feature scaler

## 💻 Usage

### Running the Application

1. **Start the Streamlit app**:
```bash
streamlit run app.py
```

2. **Access the application**:
   - The app will automatically open in your default browser
   - Default URL: `http://localhost:8501`

### First-Time Setup

1. **Register an Account**:
   - Use the sidebar registration form
   - Enter a unique username and password
   - Click "Register"

2. **Login**:
   - Enter your credentials in the login form
   - Click "Login"

### Making Predictions

1. Navigate to **"Fraud Prediction"** page
2. Fill in the transaction details:
   - Transaction amount
   - Date and time
   - Location (select from Uzbekistan regions)
   - Card type and currency
   - Authentication method
   - Behavioral metrics (velocity, distance, etc.)
3. Click **"Predict Fraud"**
4. View the prediction result and probability score
5. Prediction is automatically saved to your history

### Viewing Transaction History

1. Navigate to **"User Transaction History"** page
2. View all your past predictions in a table
3. Download history as Excel file using the download button

### Exploring the Dataset

1. Navigate to **"Dataset Information and EDA"** page
2. View dataset statistics and information
3. Explore distribution plots for numerical features
4. Analyze categorical feature distributions
5. Check target variable balance

## 🤖 Model Details

### Algorithm
**Random Forest Classifier** - An ensemble learning method that constructs multiple decision trees during training.

### Feature Engineering

1. **DateTime Features**:
   - Extract hour, day of week, and month from timestamps
   - Drop original date/time columns

2. **Categorical Encoding**:
   - One-hot encoding for categorical variables
   - Drop first category to avoid multicollinearity

3. **Feature Scaling**:
   - StandardScaler for numerical features
   - Ensures all features contribute equally to predictions

### Model Training Process

The model training is documented in `CardFraud.ipynb`:

1. **Data Loading**: Import dataset from CSV
2. **Exploratory Data Analysis**: Understand feature distributions
3. **Data Preprocessing**: Handle missing values, encode categories
4. **Feature Engineering**: Create temporal features
5. **Train-Test Split**: 80-20 split for validation
6. **Model Training**: Train Random Forest with optimal hyperparameters
7. **Model Evaluation**: Assess performance metrics
8. **Model Serialization**: Save model and scaler using joblib

### Performance Metrics
- Accuracy
- Precision
- Recall
- F1-Score
- ROC-AUC Score

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL
);
```

### Transactions Table
```sql
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    timestamp TEXT NOT NULL,
    raw_input TEXT NOT NULL,
    prediction TEXT NOT NULL,
    probability REAL NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);
```

## 🛠️ Technologies Used

- **Frontend**: Streamlit
- **Machine Learning**: scikit-learn, pandas, numpy
- **Visualization**: matplotlib, seaborn
- **Database**: SQLite3
- **Security**: hashlib (SHA-256 password hashing)
- **Data Export**: openpyxl (Excel export)
- **Model Persistence**: joblib

## 📦 Dependencies

```
streamlit
pandas
numpy
scikit-learn
matplotlib
seaborn
joblib
openpyxl
pyngrok
```

## 🔒 Security Features

- **Password Hashing**: SHA-256 encryption for stored passwords
- **Session Management**: Secure session state handling
- **SQL Injection Prevention**: Parameterized queries
- **User Isolation**: Transaction history isolated per user

## 🎯 Future Enhancements

- [ ] Add batch prediction for multiple transactions
- [ ] Implement advanced analytics dashboard
- [ ] Add email notifications for fraud alerts
- [ ] Integrate with real payment APIs
- [ ] Add model retraining pipeline
- [ ] Implement role-based access control
- [ ] Add transaction risk scoring
- [ ] Export reports in PDF format

## 🐛 Troubleshooting

### Common Issues

**Issue**: Module not found error
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt --upgrade
```

**Issue**: Database locked error
```bash
# Solution: Close all connections and restart the app
# Delete app_data.db and restart (will lose user data)
```

**Issue**: Model file not found
```bash
# Solution: Ensure random_forest_model.joblib and scaler.joblib are in the root directory
```

## 📝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- S Pushpa Latha

## 🌐 Project Links

- https://frauddetection-ksgngzmohvakdfu7hxhpjk.streamlit.app/
