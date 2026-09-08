import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def conectar_banco():
    return mysql.connector.connect(
        host = os.getenv('DATABASE_HOST'),
        port = int(os.getenv('DATABASE_PORT')),
        database = os.getenv('DATABASE_NAME'),
        user = os.getenv('DATABASE_USER'),
        password = os.getenv('DATABASE_PASSWORD'),
        ssl_ca = 'ca.pem'
    )