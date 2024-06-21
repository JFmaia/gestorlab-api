# Use a imagem base python
FROM python:3.10

# Configure o diretório de trabalho
WORKDIR /app

# Copie o arquivo de dependências
COPY requirements.txt .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Instale o cliente PostgreSQL
RUN apt-get update && apt-get install -y postgresql-client

# Copie o restante do código
COPY . .

# Comando para iniciar o aplicativo
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
