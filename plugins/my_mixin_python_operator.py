from airflow.operators.bash_operator import BaseOperator
from airflow.operators.python_operator import PythonOperator
import logging
from contrib.pagerduty import PagerDuty


class MyAlertingMixin(BaseOperator):
    ui_color = '#000'
    ui_fgcolor = '#25c151'

    """
    provide a standard way for pagerduty
    """
    def execute(self, context):
        try:
            return super(MyAlertingMixin, self).execute(context)
        except Exception as e:

            dt = context.get('execution_date')
            exe_date = dt.strftime('%y-%m-%d_%H:%M') if dt else 'UNK'
            e_type = e.__class__.__name__
            severity = PagerDuty.SEVERITY_ERROR
            message = 'Task failure {dag}.{dt} {task} {e_type}:{e_message}'.format(
                dag=self.dag.dag_id,
                dt=exe_date,
                task=self.task_id,
                e_type=e_type,
                e_message=str(e)
            )
            try:
                PagerDuty(
                    message=message,
                    severity=severity,
                    error_class=e_type,
                    payload={
                        'dag': self.dag.dag_id,
                        'task': self.task_id,
                        'execution_date': exe_date,
                        'exception': {
                            'type': e_type,
                            'message': str(e)
                        }
                    }
                ).send()
            except Exception as e1:
                logging.error('failed to call pager duty: `{}`, original error {}'.format(e1, message))
            raise


class MyMixinPythonOperator(MyAlertingMixin, PythonOperator):
    pass
