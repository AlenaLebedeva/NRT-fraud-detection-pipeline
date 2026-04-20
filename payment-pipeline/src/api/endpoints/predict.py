from fastapi import APIRouter, HTTPException, BackgroundTasks
from src.api.models import Transaction, PredictionResponse
from src.database import save_transaction, get_account_history
import pandas as pd
import numpy as np
import joblib
from datetime import datetime
import os

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_PATH = os.path.join(BASE_DIR, "models", "best_model_improved.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "models", "scaler_improved.pkl")

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

def compute_features(tx: Transaction, history_df: pd.DataFrame):
    features = {}
    features['TransactionAmount'] = tx.TransactionAmount
    features['AccountBalance'] = tx.AccountBalance
    features['hour'] = tx.Timestamp.hour
    features['day_of_week'] = tx.Timestamp.weekday()
    features['weekend'] = 1 if features['day_of_week'] >= 5 else 0

    if not history_df.empty:
        mean_amt = history_df['transaction_amount'].mean()
        std_amt = history_df['transaction_amount'].std()
        features['amount_zscore'] = (tx.TransactionAmount - mean_amt) / (std_amt if std_amt > 0 else 1)
        features['rolling_mean_amount'] = history_df['transaction_amount'].head(5).mean()
    else:
        features['amount_zscore'] = 0.0
        features['rolling_mean_amount'] = tx.TransactionAmount

    features['balance_ratio'] = tx.TransactionAmount / (tx.AccountBalance + 1e-6)
    features['is_large'] = 1 if tx.TransactionAmount > 4000 else 0
    features['hour_sin'] = np.sin(2 * np.pi * features['hour'] / 24)
    features['hour_cos'] = np.cos(2 * np.pi * features['hour'] / 24)
    features['days_since_start'] = (tx.Timestamp - datetime(2016, 1, 1)).days
    features['rolling_std_amount'] = history_df['transaction_amount'].std() if not history_df.empty else 0.0

    feature_order = [
        'TransactionAmount', 'AccountBalance', 'hour', 'day_of_week', 'weekend',
        'amount_zscore', 'balance_ratio', 'is_large', 'hour_sin', 'hour_cos',
        'days_since_start', 'rolling_mean_amount', 'rolling_std_amount'
    ]
    X = pd.DataFrame([[features[f] for f in feature_order]], columns=feature_order)
    return X

@router.post("/predict", response_model=PredictionResponse)
async def predict(transaction: Transaction, background_tasks: BackgroundTasks):
    try:
        history = get_account_history(transaction.AccountID, limit=10)
        X = compute_features(transaction, history)
        X_scaled = scaler.transform(X)
        proba = model.predict_proba(X_scaled)[0, 1]
        is_anomaly = proba > 0.5
        background_tasks.add_task(save_transaction, transaction, is_anomaly, proba, "catboost_v1")
        return PredictionResponse(
            transaction_id=transaction.TransactionID,
            is_anomaly=is_anomaly,
            anomaly_probability=float(proba),
            prediction_time=datetime.now(),
            model_version="catboost_v1"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
