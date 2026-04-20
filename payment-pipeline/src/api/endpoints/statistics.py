from fastapi import APIRouter, HTTPException
from src.api.models import StatsResponse
from src.database import get_db

router = APIRouter()

@router.get("/stats/{account_id}", response_model=StatsResponse)
async def get_stats(account_id: int):
    with get_db() as conn:
        cursor = conn.execute(
            "SELECT COUNT(*) as total, SUM(is_anomaly) as anomalies FROM transactions WHERE account_id = ?",
            (account_id,)
        )
        row = cursor.fetchone()
        if row['total'] == 0:
            raise HTTPException(status_code=404, detail="Account not found")
        cursor = conn.execute(
            "SELECT AVG(anomaly_probability) as avg_risk FROM transactions WHERE account_id = ? AND is_anomaly = 1",
            (account_id,)
        )
        risk_row = cursor.fetchone()
    return StatsResponse(
        account_id=account_id,
        total_transactions=row['total'],
        anomalies_detected=row['anomalies'] or 0,
        anomaly_rate=(row['anomalies'] / row['total']) if row['total'] > 0 else 0.0,
        average_risk_score=risk_row['avg_risk'] or 0.0
    )
