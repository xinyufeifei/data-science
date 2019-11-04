# Airflow and Postgres DB
Even though there are many documentations regarding how to install airflow, I still encountered some gotcha moments. Therefore I would like to document the steps I took to install airflow for my future reference.
## Install Postgres
Airflow requires a database to store the metadata. The default database that airflow is call sqlite. Based on the official document, this database can be easily filled up. It is recommended to use mysql or postgres database for frequent users. Therefore I decided to install Postgres on my local laptop since I used postgresql a lot during my work and I believe postgresql is a more modern sql than mysql. Because I have a mac, it is easier to use **Homebrew** to install all the gadgets.
```bash
brew install postgresql
```
The command above can install postgresql on my laptop. Then I can start postgres service and login postgres database.
```bash
brew services start postgresql
psql postgres
```
Next I created a database for airflow, called airflow, using **psql** command. The command `-l` would list all the available databases.
```
CREATE DATABASE airflow
```
At last, I typed command `exit` to logout postgres. Now I finished setting up postgres database for airflow.
## Install Airflow
The official documentation of airflow provides guidance on installing Airflow. The command is very simple.
```bash
export AIRFLOW_HOME=~/airflow
pip install apache-airflow
``` 
But the challenge is that the command would try to install all the dependencies (~30 modules). The first error I got is `xcrun: error`.

> xcrun: error: invalid active developer path (/Library/Developer/CommandLineTools), missing xcrun at: /Library/Developer/CommandLineTools/usr/bin/xcrun

The error was due to my recent OS update. I updated my OS to Catalina (V10.115). The command line tool xcode also needs to be updated accordingly, which I had not done yet. Update/install xcode is straightforward by running the following command.
```
—xcode-select --install
```
The second error happened when psycopg2, once of the dependencies, was being installed. I searched online and found the solution posted on the stack overflow worked. <https://stackoverflow.com/questions/39767810/cant-install-psycopg2-package-through-pip-install-is-this-because-of-sierra>
```
env LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" pip install psycopg2
```
I was able to install apache-airflow at this moment in a python virtual environment based python 3.7.4. I tried to install airflow using python 3.8.0, but the solution to fix the error related to psycopg2 did not work. I tried other solutions but without luck.

## Set up Airflow
### Modify config file
I opened the airflow config file at `~/airflow/airflow.cfg`, and modified the parameters of `executor` and `sql_alchemy_conn` in this config file. It will point the airflow to the postgres database I created earlier.
```
executor = LocalExecutor

sql_alchemy_conn = postgresql+psycopg2://localhost/airflow?user={your user name}
```
If you are not sure about the user name, go back to login postgres and use psql command `-l` to check all the available databases and their associated user names.

### Start Airflow webserver
Airflow provides a very neat web UI that enables users to see all the jobs(dags), trigger a job(dag), and monitor the process of tasks visually. To start the webserver and the scheduler, go to the terminals and type the following commands. I used separate terminals for each command.
```
# start the web server, default port is 8080
airflow webserver -p 8080

# start the scheduler
airflow scheduler
``` 
Then I opened a browser, typed the web address: http://localhost:8080, and then the airflow UI magically showed up! If one of the command does not work, it is highly possible that the file `airflow.cfg` is not configured properly.

### Create a DAG
DAG stands for Directed Acyclic Graph. It serves as a recipe to tell your system how to execute the tasks that are also defined in the DAG. The recipe needs to be written in python script. But Airflow provides a set of powerful operators for a wide range of tasks. For example, **bash operator** allows me to run a python script, **docker operator** allows me to run command in a container, and **python operator** allows me to call a python function. <br>
<br>
After all the tasks are defined with these operators, the tasks can be organized to be "cooked" in any order I like. Here is a example of DAG file from [Michał Karzyński's blog]<http://michal.karzynski.pl/blog/2017/03/19/developing-workflows-with-apache-airflow/>.

```python
from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

def print_hello():
    return 'Hello world!'

dag = DAG('hello_world', description='Simple tutorial DAG',
          schedule_interval='0 12 * * *',
          start_date=datetime(2017, 3, 20), catchup=False)

dummy_operator = DummyOperator(task_id='dummy_task', retries=3, dag=dag)

hello_operator = PythonOperator(task_id='hello_task', python_callable=print_hello, dag=dag)

dummy_operator >> hello_operator
```

### Execute workflow
The DAG file can be tested as a normal python script. However the test cannot guaranteed that each task can be run successfully because the tasks are executed at this point. So it is a good practice to test individual task outside of DAG before move them into DAG. Once we passed all the tests, the DAG file can be moved to the folder `~/airflow/dags`. At this moment, when the page http://localhost:8080 is refreshed, the new job would appear the Dag list.<br>

The schedule of the job should be specified in the DAG file. But the job can be manually triggered on the webpage. We need to make sure `On` button associated with the job is toggled otherwise it won't be executed.

## Summary

As a python user, I am so glad to see an ELT tool integrated with python. And I am able to build flexible data pipelines, without using third party tool, such as Jenkins. And most importantly, I can use Airflow web UI to visually check the structure of the workflow and the progress of individual tasks.<br>
 
However, the debug process is not very intuitive. In the beginning, I manually triggered the job, waited for it to finish, and checked the log when a task failed. Once I fixed the issue in my code editor, I triggered the job again. I did it repetitively until I realized the debugging process was not efficient because I had to wait for the upstream jobs to finish. Therefore I learned to test individual task before I chained them together.

It took me a couple of hours to set up everything for Airflow and understand the file structure. So far, I have been able to use Airflow to schedule jobs that involves executing python scripts and Jupyter notebooks. I am also able to schedule a task inside a docker container. I am sure that Airflow is capable of executing more complicated tasks. I am looking forward to using Airflow for those tasks.<br>