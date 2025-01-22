from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from pyspark.sql import SparkSession
import os
import csv

# Function to process the CSV
def process_csv():
    spark = SparkSession.builder \
        .appName("Airflow-PySpark") \
        .getOrCreate()

    # Read the CSV file
    input_path = "/opt/airflow/extracted_data/youtube_data/jre_data_2025-01-16.csv"
    output_folder = "/opt/airflow/transformed_data/youtube_data"


    os.makedirs(output_folder, exist_ok=True)  # Ensure the directory exists
    today = datetime.now().strftime('%Y-%m-%d')
    output_file = os.path.join(output_folder, f"jre_transformed_data_{today}.csv")

    # Read and select required data
    df = spark.read.csv(input_path, header=True)
    title_data = df.select("Title").collect()

    # Convert to a list of dictionaries
    videos = [{"Title": row["Title"]} for row in title_data]

    # Save to CSV using Python's csv module
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["Title"])
        writer.writeheader()
        writer.writerows(videos)

    print(f"Data saved successfully to {output_file}")
    spark.stop()

# Define the DAG
default_args = {
    'start_date': datetime(2025, 1, 22),
    'retries': 1,
}

with DAG(
    'pyspark_process_csv',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
) as dag:
    
    # Task to process the CSV
    process_csv_task = PythonOperator(
        task_id='process_csv_task',
        python_callable=process_csv,
    )

    process_csv_task