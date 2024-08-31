
# 📊 Projeto Streamlit com Docker - Mapa de Calor!

Este projeto é um aplicativo Streamlit containerizado com Docker, projetado para criar um mapa de calor com base em dados de latitude, longitude e concentração de pedidos.

## 🚀 Início Rápido

Siga as instruções abaixo para configurar e executar o aplicativo.

### ⚙️ Pré-requisitos

- **Docker**: Certifique-se de ter o Docker instalado. Você pode baixá-lo em [docker.com](https://www.docker.com/).

### 📥 1. Clonar o Repositório

Clone este repositório em sua máquina local:

```bash
git clone https://github.com/seu-usuario/nome-do-repositorio.git
cd nome-do-repositorio
```

### 🛠️ 2. Construir a Imagem Docker

Dentro do diretório do projeto, construa a imagem Docker com o seguinte comando:

```bash
docker build -t nome-da-imagem .
```

> Substitua `nome-da-imagem` pelo nome desejado para sua imagem Docker.

### ▶️ 3. Executar o Contêiner Docker

Após a imagem ser construída, execute o contêiner usando o comando:

```bash
docker run -p 8501:8501 nome-da-imagem
```

O aplicativo Streamlit estará disponível em seu navegador no endereço: [http://localhost:8501](http://localhost:8501).

### 📂 Estrutura do Projeto

- **src/01_atualizar_banco_de_dados.py**: Arquivo principal do aplicativo Streamlit.
- **Dockerfile**: Script de configuração para construir a imagem Docker.
- **pyproject.toml**: Arquivo de configuração do Poetry com as dependências do projeto.

### ❌ 4. Parar o Contêiner Docker

Para parar o contêiner Docker em execução, siga os seguintes passos:

1. Liste os contêineres em execução:

    ```bash
    docker ps
    ```

2. Pare o contêiner usando o `CONTAINER_ID` obtido:

    ```bash
    docker stop <CONTAINER_ID>
    ```

## ℹ️ Notas Adicionais

- **Dependências**: Verifique se o arquivo `pyproject.toml` contém todas as dependências necessárias para o aplicativo Streamlit.
- **Porta do Streamlit**: A aplicação usa a porta padrão 8501. Certifique-se de que esta porta não está sendo usada por outro serviço.



