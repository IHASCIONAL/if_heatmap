import streamlit as st

class Forms:

    def __init__(self):
        self.estado = None

    def define_state(self):
        self.estado = st.selectbox(label="Selecione a praça de interesse para ver o mapa de calor", options=["Rio de Janeiro", "SP"])
    
    def form_title(self, title):
        st.header(title)

    def submit_button(self, name):
        return st.form_submit_button(name)
        
    def create_forms(self, title):
        with st.form("form"):
            self.form_title(title)
            self.define_state()
            submitted = self.submit_button("Ver Mapa")

            if submitted:
                st.write(f"Praça selecionada: {self.estado}")

class ExcelValidatorUI:

    def __init__(self):
        self.set_page_config()

    def set_page_config(self):
        st.set_page_config(
            page_title="Validador de schema excel"
        )

    def display_header(self):
        st.title("Validador de schema excel")

    def upload_file(self):
        return st.file_uploader("Carregue seu arquivo aqui", type=["xlsx", "csv"])
    
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