import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv(".env")

# Configuração da conexão com o banco de dados
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_DB = os.getenv('POSTGRES_DB')

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

class Forms:

    def __init__(self):
        self.estado = None
        self.shift = None

    def define_state(self):
        self.estado = st.selectbox(label="Selecione a praça de interesse para ver o mapa de calor", options=["Rio de Janeiro", "SP"])

    def define_shift(self):
        self.shift = st.selectbox(label="Selecione o turno", options=['MANHA', 'ALMOCO', 'TARDE', 'CEIA', 'JANTAR', 'MADRUGADA'])
    
    def form_title(self, title):
        st.header(title)

    def submit_button(self, name):
        return st.form_submit_button(name)
        
    def create_forms(self, title):
        with st.form("form"):
            self.form_title(title)

            col1, col2 = st.columns(2)

            with col1:
                self.define_state()
            with col2:
                self.define_shift()
            
            submitted = self.submit_button("Ver Mapa")

            if submitted:
                st.write(f"Praça selecionada: {self.estado}")

class ExcelValidatorUI:

    def __init__(self):
        self.set_page_config()

    def set_page_config(self):
        st.set_page_config(
            page_title="Interface para atualizar o mapa de calor"
        )

    def display_header(self):
        st.title("Atualizar Mapa de Calor")

    def upload_file(self):
        return st.file_uploader("Carregue o arquivo atualizado aqui", type=["xlsx", "csv"])
    
    def display_results(self, result ,erros):
        if erros:
            for erro in erros:
                st.error(f"Erro na validação: {erro}")
        else:
            st.success("O schema do arquivo Excel está correto!")
    
    def display_save_button(self):
        return st.button("Salvar no banco de dados")
    
    def display_wrong_message(self):
        return st.error("Necessário corrigir a planilha!")
    
    def display_success_message(self):
        return st.success("Dados salvos com sucesso no banco de dados!")