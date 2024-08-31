import streamlit as st
import requests
from backend.backend import HeatMapGenerator, DataFetcher

class Forms:

    def __init__(self):
        self.estado = None
        self.shift = None
    
    def fetch_logistic_regions(self):
        try:
            response = requests.get('http://localhost:5000/logistic-regions')  # URL do seu endpoint Flask
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"Erro ao carregar as regiões logísticas: {str(e)}")
            return []

    def define_state(self):
        logistic_regions = self.fetch_logistic_regions()
        if logistic_regions:
            self.estado = st.selectbox(label="Selecione a praça de interesse para ver o mapa de calor", options=logistic_regions)

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
                st.write(f"Praça selecionada: {self.estado}""")
                st.write(f"Turno selecionado: {self.shift}")

                data_fetcher = DataFetcher()
                df = data_fetcher.fetch_all_data()

                filtered_df = df[
                    (df['logistic_region'] == self.estado)&
                    (df['shift'] == self.shift)
                    ]
                
                heatmap_generator = HeatMapGenerator(filtered_df)
                heatmap_map = heatmap_generator.create_heatmap()
                st.components.v1.html(heatmap_map._repr_html_(), height=600)




    

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