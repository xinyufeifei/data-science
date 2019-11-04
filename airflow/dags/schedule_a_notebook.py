import os
import datetime
import airflow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

dag = DAG(dag_id='notebook_scheduler',
          description='Example code to schedule a notebook',
          start_date=airflow.utils.dates.days_ago(2),
          schedule_interval='0 0 * * *')

dummy_operator = DummyOperator(task_id='dummy_task', retries=3, dag=dag)

today_date = datetime.datetime.strftime(datetime.datetime.today(), '%Y%m%d')
current_path = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(current_path, 'notebooks/us_unemployment_rate_map/visualize_unemployment_rate_plotly.ipynb')
output_path = os.path.join(current_path, f'notebooks/output/out_{today_date}.ipynb')

print(current_path)

run_this = BashOperator(
    task_id='run_example_notebook',
    bash_command=f'papermill {input_path} {output_path}',
    dag=dag
)

dummy_operator >> run_this