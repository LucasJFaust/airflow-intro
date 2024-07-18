# Primeiro temos que importar a biblioteca que faz com que o Airflow reconheça que esse arquivo é uma DAG:
from airflow import DAG

# Importanto o operador do postgree:
from airflow.providers.postgres.operators.postgres import PostgresOperator

# Importando o sensor
from airflow.providers.http.sensors.http import HttpSensor

# Importamos o datetime para configurar o startdate
from datetime import datetime

# Agora vamos instânciar o objeto DAG, com o gerenciador de contexto with
with DAG ('user_processing', start_date=datetime(2024, 1, 1), schedule_interval='@daily', catchup=False) as DAG:
    # Agora vamos criar a nossa primeira task. Que vai ser um CREAT TABLE. Com o CREAT TABLE nos vamos usar operador do Postgree
    # para executar uma requisição SQL no DB Postgree e criar uma tabela.
    # Criando uma variável com o perador do postgres
    create_table = PostgresOperator(
        task_id = 'create_table',
        # Definindo a conexão:
        postgres_conn_id = 'postgres',
        # Requisição SQL:
        sql = """
            CREATE TABLE IF NOT EXISTS users (
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                country TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL
            );
        """
    )
    # Criando uma nova variável para receber o sensor:
    is_api_available = HttpSensor(
        task_id = 'is_api_available',
        http_conn_id = 'user_api',
        endpoint = 'api/'
    )