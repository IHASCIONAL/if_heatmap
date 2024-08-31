FROM python:3.12.5
RUN pip install poetry
COPY . /src
WORKDIR /src
RUN poetry install
EXPOSE 8501
ENTRYPOINT ["poetry", "run", "streamlit", "run", "src/01_atualizar_banco_de_dados.py", "--server.port=8501", "--server.address=0.0.0.0"]