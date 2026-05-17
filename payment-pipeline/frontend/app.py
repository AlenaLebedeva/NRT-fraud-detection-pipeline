import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import random

API_URL = "http://localhost:8000"

st.set_page_config(page_title='Payment Fraud Detector', layout='wide')
st.title('Обнаружение мошеннических платежей')

tab1, tab2, tab3 = st.tabs(['Проверить транзакцию', 'Статистика счёта', 'Мониторинг'])

with tab1:
    st.header('Ручная проверка транзакции')
    col1, col2 = st.columns(2)
    with col1:
        tx_id = st.number_input('Transaction ID', value=random.randint(100000, 999999))
        acc_id = st.number_input('Account ID', value=random.randint(1000, 10000))
        tx_type = st.selectbox('Transaction Type', ['PAYMENT', 'TRANSFER', 'CASH_OUT', 'CASH_IN', 'DEBIT'])
        amount = st.number_input('Amount', value=50000.0)
    with col2:
        old_balance_org = st.number_input('Old Balance (Sender)', value=100000.0)
        new_balance_orig = st.number_input('New Balance (Sender)', value=50000.0)
        old_balance_dest = st.number_input('Old Balance (Receiver)', value=0.0)
        new_balance_dest = st.number_input('New Balance (Receiver)', value=0.0)
        step = st.number_input('Step (hours from start)', value=500)

    if st.button('Predict'):
        payload = {
            'TransactionID': tx_id,
            'AccountID': acc_id,
            'Timestamp': datetime.now().isoformat(),
            'TransactionType': tx_type,
            'TransactionAmount': amount,
            'AccountBalance': new_balance_orig,
            'OldBalanceOrg': old_balance_org,
            'NewBalanceOrig': new_balance_orig,
            'OldBalanceDest': old_balance_dest,
            'NewBalanceDest': new_balance_dest,
            'Step': step
        }
        response = requests.post(f'{API_URL}/predict', json=payload)
        if response.status_code == 200:
            res = response.json()
            st.success(f"Предсказание: {'Аномалия' if res['is_anomaly'] else 'Норма'}")
            st.metric('Вероятность мошенничества', f"{res['anomaly_probability']:.2%}")
        else:
            st.error('Ошибка API')

with tab2:
    st.header('Статистика по счёту')
    acc_id_stats = st.number_input('Account ID', key='stats_id', value=1000)
    if st.button('Показать статистику'):
        response = requests.get(f'{API_URL}/stats/{acc_id_stats}')
        if response.status_code == 200:
            stats = response.json()
            col1, col2, col3 = st.columns(3)
            col1.metric('Всего транзакций', stats['total_transactions'])
            col2.metric('Аномалий обнаружено', stats['anomalies_detected'])
            col3.metric('Доля аномалий', f"{stats['anomaly_rate']:.2%}")
        else:
            st.error('Счёт не найден')

with tab3:
    st.header('Симуляция потока транзакций')
    if st.button('Запустить симуляцию (10 транзакций)'):
        for i in range(10):
            payload = {
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
            response = requests.post(f'{API_URL}/predict', json=payload)
            if response.ok:
                st.write(f"Транзакция {i + 1}: {'Аномалия' if response.json()['is_anomaly'] else 'Норма'}")
            else:
                st.write(f'Транзакция {i + 1}: ошибка')