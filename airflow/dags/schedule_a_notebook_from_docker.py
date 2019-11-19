import os
from datetime import datetime, timedelta
import airflow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.docker_operator import DockerOperator


default_args = {
    'description'       : 'Use DockerOperator',
    'depend_on_past'    : False,
    'start_date'        : datetime(2018, 1, 3),
    'email_on_failure'  : False,
    'email_on_retry'    : False,
    'retries'           : 0,
    'retry_delay'       : timedelta(minutes=5)
}



today_date = datetime.strftime(datetime.today(), '%Y%m%d')
current_path = os.path.dirname(os.path.abspath(__file__))
input_path = 'notebooks/us_unemployment_rate_map/visualize_unemployment_rate_plotly.ipynb'
output_path = f'notebooks/output/out_{today_date}.ipynb'

print(current_path)

with DAG('docker_dag', default_args=default_args,
         schedule_interval='0 0 * * *', catchup=False) as dag:

    dummy_operator = DummyOperator(task_id='dummy_task', retries=3)

    run_this = DockerOperator(
        task_id='run_example_notebook_inside_docker',
        image='supergirl:latest',
        api_version='auto',
        auto_remove=True,
        command=f'papermill {input_path} {output_path}',
        docker_url='unix://var/run/docker.sock',
        network_mode='bridge'
    )

    dummy_operator >> run_this