from datetime import timedelta

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this tooperate!
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

# these dags will get pass to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
	'owner': 'airflow',
	'depends_on_past': False,
	'email': ['airflow@example.com'],
	'email_on_failure': False,
	'email_on_retry': False,
	'retries': 1,
	'retry_delay': timedelta(minutes=5),
	# 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2021, 4, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}

# instanriate a DAG
dag = DAG(
	'tutorial',
	default_args = default_args,
	description = 'A simple tutorial DAG',
	schedule_interval = timedelta(days=1),
	start_date = days_ago(2),
	tags = ['example']
)

# TASKS
t1 = BashOperator(
	task_id = 'print_date',
	bash_command = 'date',
	dag = dag
)

t2 = BashOperator(
	task_id = 'sleep',
	depends_on_past = False,
	bash_command = 'sleep 5',
	retries = 3,
	dag=dag
	)

# Templating with Jinja
templated_command = """
	{% for i in range(5) %}
		echo "{{ ds }}"
		echo "{{ macro.ds_add(ds, 7) }}"
		echo "{{ params.my_param }}"
	{% endfor %}
"""

t3 = BashOperator(
	task_id = 'templated',
	depends_on_past = False,
	bash_command = templated_command,
	params = {'my_param': 'Parameter I passed in'},
	dag = dag
)

# Adding DAG and documentation
dag.doc_md = __doc__

t1.doc_md = """\
#### Task Documentation
You can document your task using the attributes `doc_md` (markdown),
`doc` (plain text), `doc_rst`, `doc_json`, `doc_yaml` which gets
rendered in the UI's Task Instance Details page.
![img](http://montcs.bloomu.edu/~bobmon/Semesters/2012-01/491/import%20soul.png)
"""

# setting dependencies
t1 >> [t2, t3]

# or t1.set_downstream([t2, t3])