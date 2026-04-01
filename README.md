- Тема ВКР: "Разработка нагруженного в режиме близкого к реальному времени конвейера данных поставки платёжной информации, с сохранением истории платежей"
- Тема ВКР на английском языке: "Development of an NRT (Near Real-Time) Data Pipeline for the Supply of Payment Information, While Maintaining the Payment History"
- ФИО студента: Лебедева Алёна Павловна
- ФИО научного руководителя: Заигрин Вадим Валерьевич

# Верхнеуровневый план работ (с предположительными дедлайнами):

1. Обзор источников информации и выбор источников данных - 25.01.2026
2. Анализ структуры данных - 28.02.2026
3. Анализ и выбор технологий для создания конвейера данных - 15.03.2026
4. Разработка архитектуры конвейера - 28.03.2026
5. Разработка модуля приема данных - 07.04.2026
6. Разработка модуля потоковой обработки данных - 14.04.2026
7. Реализация механизмов сохранения истории платежей - 30.04.2026
8. Разработка сервиса для доступа к готовым данным - 14.05.2026
9. Тестирование и доработка готового конвейера - 21.05.2026
10. Написание ВКР с реализацией результатов работы - 31.05.2026

## Данные

- Источник данных: [Financial Transactions Dataset for Analysis](https://www.kaggle.com/datasets/mdhossanr/financial-transactions-dataset-for-analysis) (Kaggle)
- Описание: синтетический датасет, содержащий 37 417 транзакций с информацией об идентификаторах счетов, типе операции, сумме, балансе и временных метках.
- Ноутбук с EDA: [`EDA_final_project.ipynb`](EDA_final_project.ipynb) — разведочный анализ данных, включая визуализации и выводы.

## Модель

- После проведенной работы был выбран RandomForest с параметрами: {'class_weight': 'balanced', 'max_depth': 5, 'min_samples_leaf': 2, 'min_samples_split': 5, 'n_estimators': 50}. Данная модель показала наилучшее качество. В качестве метрик выбраны recall, precision, F1-score и ROC-AUC
- Ссылка на ноутбук с baseline: [final_project_baseline_metrics.ipynb](https://github.com/AlenaLebedeva/hse_abd_final_qualifying_work/blob/e7c765a456b52cdc32ed1ba504bd72ad77fb6e37/payment-pipeline/src/notebooks/final_project_baseline_metrics.ipynb)

## Сервис

В папке [payment-pipeline](https://github.com/AlenaLebedeva/hse_abd_final_qualifying_work/tree/e78145365aec4dc0cf1d63d0c62965b63821ad89/payment-pipeline) представлена схема будущего сервиса, которая включает в себя ноутбуки, модели, FastAPI и модели
