
"""
Apache Airflow introduced the TaskFlow API which allows you to create tasks using python decorators like @task. This is a cleaner and more intuitive way of writing tasks without needing to manually use operators like PythonOperator. Let us see how to modify the previous code used in the "maths_operation.py" file to use the TaskFlow API.

"""



from airflow import DAG
from airflow.decorators import task
from datetime import datetime

#Defining the DAG
with DAG(
    dag_id = 'math_sequence_dag_with_taskflow',
    start_date = datetime(2025, 1, 1),
    schedule_interval = '@once',
    catchup = False
) as dag:
    
    #Task-1: Start with the initial number
    @task
    def start_num():
        initial_val = 10
        print(f"Starting Number: {initial_val}")
        return initial_val
    #Task-2: Add 5 to the number
    @task
    def add_five(num):
        new_value = num + 5
        print(f"Adding 5 to {num} = {new_value}")
        return new_value
    #Task-3: Multiply the result by 2
    @task
    def multiply_by_two(num):
        new_value = num * 2
        print(f"Multiplying {num} by 2 = {new_value}")
        return new_value
    #Task-4: Subtract 3 from the result
    @task
    def subtract_three(num):
        new_value = num - 3
        print(f"Subtracting 3 from {num} = {new_value}")
        return new_value
    #Task-5: Compute the square of the result
    @task
    def square_number(num):
        new_value = num ** 2
        print(f"Squaring {num}^2 = {new_value}")
        return new_value
    
    #Set task dependencies using the TaskFlow API
    start_value = start_num()
    added_value = add_five(start_value)
    multiplied_value = multiply_by_two(added_value)
    subtracted_value = subtract_three(multiplied_value)
    squared_value = square_number(subtracted_value)

     

