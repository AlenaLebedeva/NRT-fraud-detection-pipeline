import requests
import random
import time
from datetime import datetime

API_URL = 'http://localhost:8000/predict'

def generate():
    return {
        'TransactionID': random.randint(100000, 999999),
        'AccountID': random.randint(1000, 10000),
        'Timestamp': datetime.now().isoformat(),
        'TransactionType': random.choice(['PAYMENT', 'TRANSFER', 'CASH_OUT', 'CASH_IN', 'DEBIT']),
        'TransactionAmount': round(random.uniform(1000, 500000), 2),
        'AccountBalance': round(random.uniform(5000, 500000), 2),
        'OldBalanceOrg': round(random.uniform(10000, 1000000), 2),
        'NewBalanceOrig': round(random.uniform(1000, 500000), 2),
        'OldBalanceDest': round(random.uniform(0, 100000), 2),
        'NewBalanceDest': round(random.uniform(0, 100000), 2),
        'Step': random.randint(1, 743)
    }

if __name__ == '__main__':
    print('Генератор запущен. Нажмите Ctrl+C для остановки.')
    while True:
        tx = generate()
        resp = requests.post(API_URL, json=tx)
        print(f"{tx['TransactionID']}: {'Anomaly' if resp.json()['is_anomaly'] else 'Normal'} ({resp.json()['anomaly_probability']:.2f})")
        time.sleep(2)