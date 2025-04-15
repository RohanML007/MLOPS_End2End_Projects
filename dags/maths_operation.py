from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

"""
We'll define a DAG where the tasks are as follows:

Task-1: Start with an initial number (e.g., 10).
Task-2: Add 5 to the number.
Task-3: Multiply the result by 2.
Task-4: Subtract 3 from the result.
Task-5: Compute the square of the result. 

"""

#Defining function for each task
def start_number(**context):
    context["ti"].xcom_push(key='current_val', value=10)
    print("Starting with initial number: 10")

def add_five(**context):
    current_val = context["ti"].xcom_pull(key='current_val', task_ids='start_task')
    new_value = current_val + 5
    context["ti"].xcom_push(key='current_val', value=new_value)
    print(f"Adding 5 to {current_val} = {new_value}") 

def multiply_by_two(**context):
    current_val =  context["ti"].xcom_pull(key='current_val', task_ids='add_task')
    new_value = current_val * 2
    context["ti"].xcom_push(key='current_val', value=new_value)
    print(f"Multiplying {current_val} by 2 = {new_value}")

def subtract_three(**context):
    current_val = context["ti"].xcom_pull(key='current_val', task_ids='multiply_task')
    new_value = current_val - 3
    context["ti"].xcom_push(key='current_val', value=new_value)
    print(f"Subtracting 3 from {current_val} = {new_value}")

def square_number(**context):
    current_val = context["ti"].xcom_pull(key='current_val', task_ids='subtract_task')
    new_value = current_val ** 2
    print(f"Squaring {current_val}^2 = {new_value}")

#Defining the DAG
with DAG(
    dag_id = 'maths_sequence_dag',
    start_date = datetime(2025, 1, 1),
    schedule_interval = '@once',
    catchup = False
) as dag:
    #Defining tasks
    start_task = PythonOperator(
        task_id = 'start_task',
        python_callable = start_number,  #function name
        provide_context = True  #providing context from one task to another using xcom
    )
    add_task = PythonOperator(
        task_id = 'add_task',
        python_callable = add_five,
        provide_context = True
    )
    multiply_task = PythonOperator(
        task_id = 'multiply_task',
        python_callable = multiply_by_two,
        provide_context = True
    )
    subtract_task = PythonOperator(
        task_id = 'subtract_task',
        python_callable = subtract_three,
        provide_context = True
    )
    square_task = PythonOperator(
        task_id = 'square_task',
        python_callable = square_number,
        provide_context = True
    )

    #Setting task dependencies
    start_task >> add_task >> multiply_task >> subtract_task >> square_task


