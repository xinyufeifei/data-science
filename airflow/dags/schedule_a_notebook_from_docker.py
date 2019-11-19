import os
from datetime import datetime, timedelta
import airflow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
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

with DAG('docker_dag', default_args=default_args,
         schedule_interval='0 0 * * *', catchup=False) as dag:

    dummy_operator = DummyOperator(task_id='dummy_task', retries=3)

    run_this = DockerOperator(
        task_id='run_example_notebook_inside_docker',
        image='supergirl:latest',
        api_version='auto',
        auto_remove=True,
        docker_url='unix://var/run/docker.sock',
        network_mode='bridge',
        volumes=['/Users/qzeng/git/data-science/docker/supergirl:/supergirl']
    )

    dummy_operator >> run_this