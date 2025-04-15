from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

#Defining Task-1
def preprocess_data():
    print("Preprocessing data...")

#Defining Task-2
def train_model():
    print("Training model...")

#Defining Task-3
def evaluate_model():
    print("Evaluating model...")

#Defining Task-4 (DAG)
with DAG(
    'ml_pipeline',
    start_date=datetime(2025, 1, 1),
    schedule_interval='@weekly',
) as dag:
    #Defining the tasks
    preprocess = PythonOperator(task_id="preprocess_task", python_callable=preprocess_data)
    train = PythonOperator(task_id="train_task", python_callable=train_model)
    evaluate = PythonOperator(task_id="evaluate_task", python_callable=evaluate_model)

    #Set dependencies
    preprocess >> train >> evaluate
    #This means that the "train" task will only run after the "preprocess" task is complete, and the "evaluate" task will only run after the "train" task is complete. 