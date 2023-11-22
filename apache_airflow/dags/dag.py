
# bibliotecas

from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash_operator import BashOperator

# criação do dag

with DAG(
    dag_id = 'dag',
    start_date = days_ago(1),
    schedule_interval = '@daily'
) as dag:

    tarefa_1 = EmptyOperator(task_id = 'tarefa_1')
    tarefa_2 = EmptyOperator(task_id = 'tarefa_2')
    tarefa_3 = EmptyOperator(task_id = 'tarefa_3')
    tarefa_4 = BashOperator(
        task_id = 'cria_pasta',
        # criar uma pasta para cada vez que rodar, e o nome da pasta vai ter a data correspondente
        bash_command = 'mkdir -p "G:\Meu Drive\5. Cursos\programming\tools-functions\apache_airflow\pasta={{data_interval_end}}"' 
    )

    tarefa_1 >> [tarefa_2, tarefa_3]
    tarefa_3 >> tarefa_4