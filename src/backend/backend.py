import pandas as pd
from backend.contrato import Orders
from pydantic import ValidationError
import folium
from folium.plugins import HeatMap
from backend.config import get_database_connection


class FileLoader:
    def __init__(self):
        self.dataframe = pd.DataFrame()

    def load(self, uploaded_file):
        """
        Carrega o arquivo com base no tipo identificado.

        Args:
            uploaded_file (UploadedFile): O arquivo carregado via Streamlit.

        Returns:
            DataFrame: DataFrame carregado ou DataFrame vazio em caso de erro.
        """
        try:
            # Verifica o tipo do arquivo pelo seu nome ou extensão
            if uploaded_file.name.endswith('.csv'):
                self.dataframe = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx') or uploaded_file.name.endswith('.xls'):
                self.dataframe = pd.read_excel(uploaded_file)
            else:
                raise ValueError("Formato de arquivo não suportado. Por favor, carregue um arquivo CSV ou Excel.")

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
        # Carregar o arquivo
        dataframe = self.file_loader.load(uploaded_file)
        if dataframe.empty:
            return pd.DataFrame(), False, "Erro ao carregar o arquivo."

        # Validar o DataFrame
        validated_df, is_valid, errors = self.dataframe_validator.validate(dataframe)

        return validated_df, is_valid, errors

class RefreshDataBase:

    def refresh_database(self, df):
        # Obter a conexão com o banco de dados
        engine = get_database_connection()
        with engine.connect() as conn:
            df.to_sql("orders", con=conn, if_exists='replace', index=False)

class DataFetcher:
    def __init__(self):
        self.engine = get_database_connection()

    def _execute_query(self, query):
        """Executes a SQL query and returns the result as a DataFrame."""
        with self.engine.connect() as conn:
            return pd.read_sql(query, conn)

    def fetch_all_data(self):
        query = "SELECT * FROM orders;"
        return self._execute_query(query)

    def fetch_logistic_regions(self):
        query = "SELECT DISTINCT logistic_region FROM orders;"
        df = self._execute_query(query)
        return df['logistic_region'].tolist()


class HeatMapGenerator:

    def __init__(self, df):
        self.df = df
        self.central_lat = None
        self.central_lon = None
        self.map = None

    def get_mean_lat_lon(self):
        # Inicializar o mapa
        self.central_lat = self.df['origin_latitude'].mean()
        self.central_lon = self.df['origin_longitude'].mean()
    
    def initialize_map(self):
        self.map = folium.Map(location=[self.central_lat, self.central_lon], zoom_start=12)
    
    def generate_map(self):
        heat_data = [[row['origin_latitude'], row['origin_longitude'], row['Pedidos']] for index, row in self.df.iterrows()]
        HeatMap(heat_data).add_to(self.map)

    def create_heatmap(self):
        # Executar a criação do mapa e do heatmap
        self.get_mean_lat_lon()
        self.initialize_map()
        self.generate_map()
        return self.map