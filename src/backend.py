import pandas as pd
from contrato import Orders
from pydantic import ValidationError

class FileTypeIdentifier:
    def __init__(self):
        self.dtype = 'unknown'

    def identify(self, uploaded_file):
        """
        Identifica o tipo de arquivo com base no conteúdo do arquivo carregado.

        Args:
            uploaded_file (UploadedFile): O arquivo carregado via Streamlit.

        Returns:
            str: Tipo do arquivo ('csv', 'xlsx', ou 'unknown').
        """
        try:
            # Tenta ler o arquivo como um CSV
            pd.read_csv(uploaded_file)
            self.dtype = 'csv'
        except Exception:
            try:
                # Tenta ler o arquivo como um Excel
                pd.read_excel(uploaded_file)
                self.dtype = 'xlsx'
            except Exception:
                self.dtype = 'unknown'
        
        return self.dtype

class FileLoader:
    def __init__(self):
        self.dataframe = pd.DataFrame()

    def load(self, uploaded_file, dtype):
        """
        Carrega o arquivo com base no tipo identificado.

        Args:
            uploaded_file (UploadedFile): O arquivo carregado via Streamlit.
            dtype (str): Tipo do arquivo ('csv' ou 'xlsx').

        Returns:
            DataFrame: DataFrame carregado ou DataFrame vazio em caso de erro.
        """
        try:
            if dtype == 'csv':
                self.dataframe = pd.read_csv(uploaded_file)
            elif dtype == 'xlsx':
                self.dataframe = pd.read_excel(uploaded_file)
            else:
                raise ValueError("Tipo de arquivo desconhecido.")
        except Exception as e:
            print(f"Erro ao carregar o arquivo: {str(e)}")
            self.dataframe = pd.DataFrame()

        return self.dataframe
    

class DataFrameValidator:
    def __init__(self):
        self.errors = []

    def validate(self, dataframe):
        """
        Valida as linhas de um DataFrame de acordo com o schema Pydantic.

        Args:
            dataframe (DataFrame): O DataFrame a ser validado.

        Returns:
            Tuple: (DataFrame, bool, List) ou (DataFrame vazio, str) em caso de erro.
        """
        self.errors = []

        # Verifica por colunas extras no DataFrame
        extra_cols = set(dataframe.columns) - set(Orders.model_fields.keys())
        if extra_cols:
            return pd.DataFrame(), False, [f"Colunas extras detectadas: {', '.join(extra_cols)}"]

        # Validar cada linha com o schema Orders
        for index, row in dataframe.iterrows():
            try:
                # Valida a linha como um dicionário
                _ = Orders(**row.to_dict())  
            except ValidationError as ve:
                # Captura e formata os erros de validação de Pydantic
                for error in ve.errors():
                    field = error.get('loc', ['unknown'])[0]
                    message = error.get('msg', 'Erro desconhecido')
                    self.errors.append(f"Erro na linha {index + 2}, campo '{field}': {message}")
            except Exception as e:
                # Captura erros inesperados
                self.errors.append(f"Erro inesperado na linha {index + 2}: {str(e)}")  # Converte para string

        return dataframe, not bool(self.errors), self.errors


class ProcessDataController:
    def __init__(self):
        self.file_type_identifier = FileTypeIdentifier()
        self.file_loader = FileLoader()
        self.dataframe_validator = DataFrameValidator()

    def process_data(self, uploaded_file):
        """
        Processa o arquivo carregado, identificando o tipo, carregando o conteúdo e validando.

        Args:
            uploaded_file (UploadedFile): O arquivo carregado via Streamlit.

        Returns:
            Tuple: (DataFrame, bool, List) ou (DataFrame vazio, str) em caso de erro.
        """
        # Identificar o tipo de arquivo
        file_type = self.file_type_identifier.identify(uploaded_file)
        if file_type == 'unknown':
            return pd.DataFrame(), False, "Tipo de arquivo desconhecido."

        # Carregar o arquivo
        dataframe = self.file_loader.load(uploaded_file, file_type)
        if dataframe.empty:
            return pd.DataFrame(), False, "Erro ao carregar o arquivo."

        # Validar o DataFrame
        validated_df, is_valid, errors = self.dataframe_validator.validate(dataframe)

        return validated_df, is_valid, errors
