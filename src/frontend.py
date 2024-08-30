import streamlit as st

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