from pydantic import BaseModel
from datetime import datetime

class Transaction(BaseModel):
    TransactionID: int
    AccountID: int
    Timestamp: datetime
    TransactionType: str
    TransactionAmount: float
    AccountBalance: float

class PredictionResponse(BaseModel):
    transaction_id: int
    is_anomaly: bool
    anomaly_probability: float
    prediction_time: datetime
    model_version: str

class StatsResponse(BaseModel):
    account_id: int
    total_transactions: int
    anomalies_detected: int
    anomaly_rate: float
    average_risk_score: float
