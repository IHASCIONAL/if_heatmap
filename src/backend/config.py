import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Carregar variáveis de ambiente
load_dotenv(".env")

def get_database_connection():
    # Lê as variáveis de ambiente
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT')
    POSTGRES_DB = os.getenv('POSTGRES_DB')

    # Cria a URL de conexão com o banco de dados
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

    # Cria e retorna o engine SQLAlchemy
    return create_engine(DATABASE_URL)
