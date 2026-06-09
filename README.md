# NRT Fraud Detection Pipeline

**Конвейер данных для обнаружения мошеннических транзакций в режиме, близком к реальному времени (NRT)**

[![Python 3.10](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![ML](https://img.shields.io/badge/ML-RandomForest-orange.svg)](https://scikit-learn.org/)

---

## Ключевые результаты

| Метрика | Значение |
|---------|----------|
| **F1-score** | 0.855 |
| **Precision** | 97.3% |
| **Recall** | 76.3% |
| **Производительность** | 800 RPS, задержка <50 мс |
| **Объём данных** | 6.3 млн транзакций |

> **Лучшая модель:** Random Forest (без SMOTE) — оптимальный баланс точности и полноты без переобучения.

---

## Архитектура

Генератор/Клиент → FastAPI (/predict) → Random Forest → SQLite ← Streamlit UI
↓
Ответ (аномалия + вероятность)


### Стек технологий

| Компонент | Технология |
|-----------|------------|
| API | FastAPI |
| ML | scikit-learn (Random Forest) |
| Хранилище | SQLite |
| UI | Streamlit |
| Генератор нагрузки | Python (asyncio) |

---

## Модели ML: сравнение

### На реальных данных (6.3M транзакций, 0.13% мошенничества)

| Модель | F1 | Precision | Recall | Переобучение |
|--------|----|-----------|---------|---------------|
| **Random Forest (без SMOTE)** | **0.855** | **0.973** | 0.763 | 0.027 |
| Random Forest + SMOTE | 0.781 | 0.681 | 0.915 | 0.219 |
| XGBoost + SMOTE | 0.696 | 0.539 | 0.982 | 0.299 |
| LightGBM | 0.502 | 0.337 | 0.982 | 0.006 |

**Вывод:** SMOTE на сверхразбалансированных данных (0.13%) приводит к переобучению. Random Forest без балансировки даёт лучший production-ready результат.

---

## Запуск

```bash
# 1. Установка зависимостей
pip install -r requirements.txt

# 2. Запуск API (http://127.0.0.1:8000)
uvicorn src.api.endpoints.main:app --reload

# 3. Запуск UI (в другом терминале)
streamlit run frontend/app.py

# 4. (Опционально) Генератор потока транзакций
python generator.py
```

Документация API автоматически доступна по адресу: http://127.0.0.1:8000/docs

## Структура репозитория
<pre>
payment-pipeline/
├── src/
│   ├── api/               # FastAPI (endpoints, models, database)
│   ├── models/            # Обученные модели (best_model_real.pkl)
│   └── notebooks/         # Jupyter ноутбуки с EDA и экспериментами
├── frontend/              # Streamlit UI (app.py)
├── data/                  # SQLite база (создаётся автоматически)
├── requirements.txt       # Зависимости Python
├── generator.py           # Скрипт для генерации потока транзакций
└── README.md
</pre>
  
## Данные

### 1. Синтетический датасет (отработка методологии)
- **Источник:** [Financial Transactions Dataset for Analysis](https://www.kaggle.com/datasets/mdhossanr/financial-transactions-dataset-for-analysis) (Kaggle)
- **Размер:** 37 417 транзакций
- **Целевая переменная:** создана искусственно (z-score > 2.5 или интервал < 300 сек), доля аномалий увеличена до 2%.

### 2. Реальный датасет (апробация)
- **Источник:** [Online Payments Fraud Detection](https://www.kaggle.com/datasets/rupakroy/online-payments-fraud-detection-dataset) (Kaggle)
- **Размер:** 6 362 620 транзакций
- **Доля мошенничества:** 0.13% (естественный сильный дисбаланс)
- **Целевая переменная:** `isFraud` (готовая метка)

### Тестирование производительности
- Пропускная способность: до 800 запросов/сек
- Средняя задержка: < 50 мс
- Сохранение истории: все транзакции записываются в SQLite

## Результаты
- Лучшая модель для production Random Forest (без SMOTE) на реальном датасете: F1=0.855, Precision=0.973, Recall=0.763.
- Разработанный конвейер готов к промышленной эксплуатации (API, UI, генератор, хранилище).
- Применение SMOTE на реальных данных привело к переобучению – важное наблюдение для будущих исследований.
