from fastapi import APIRouter, HTTPException, BackgroundTasks
from src.api.models import Transaction, PredictionResponse
from src.api.database import save_transaction, get_account_history
import pandas as pd
import joblib
from datetime import datetime
import os

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_PATH = os.path.join(BASE_DIR, "models", "best_model_real.pkl")

model = joblib.load(MODEL_PATH)

type_mapping = {
    'PAYMENT': 3,
    'TRANSFER': 4,
    'CASH_OUT': 1,
    'CASH_IN': 0,
    'DEBIT': 2
}

def compute_features(tx: Transaction, history_df: pd.DataFrame):

    features = {
        'amount': tx.TransactionAmount,
        'oldbalanceOrg': tx.OldBalanceOrg,
        'newbalanceOrig': tx.NewBalanceOrig,
        'oldbalanceDest': tx.OldBalanceDest,
        'newbalanceDest': tx.NewBalanceDest,
        'step': tx.Step,
        'type_encoded': type_mapping.get(tx.TransactionType, 3)
    }
    X = pd.DataFrame([features])
    return X

@router.post("/predict", response_model=PredictionResponse)
async def predict(transaction: Transaction, background_tasks: BackgroundTasks):
    try:

        history = get_account_history(transaction.AccountID, limit=10)
        X = compute_features(transaction, history)

        proba = model.predict_proba(X)[0, 1]
        is_anomaly = proba > 0.5
        background_tasks.add_task(save_transaction, transaction, is_anomaly, proba, "rf_real_v1")
        return PredictionResponse(
            transaction_id=transaction.TransactionID,
            is_anomaly=is_anomaly,
            anomaly_probability=float(proba),
            prediction_time=datetime.now(),
            model_version="rf_real_v1"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))