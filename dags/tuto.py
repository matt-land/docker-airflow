"""
Code that goes along with the Airflow located at:
http://airflow.readthedocs.org/en/latest/tutorial.html
"""
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

#from plugins.my_override_python_operator import MyOverridePythonOperator as PythonOperator
#from plugins.my_mixin_python_operator import MyMixinPythonOperator as PythonOperator

from datetime import datetime, timedelta


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2015, 6, 1),
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}


def raise_exception():
    raise RuntimeError('simulated exception')


dag = DAG("tutorial",
          default_args=default_args,
          schedule_interval=timedelta(1),
          catchup=False
          )


t1 = PythonOperator(
    task_id="exceptional_task",
    python_callable=raise_exception,
    dag=dag
)

