FROM python:3.10-slim

# Define o diretório de trabalho
WORKDIR /app

# Copie o arquivo de dependências e instale as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instale o cliente PostgreSQL se necessário
RUN apt-get update && apt-get install -y postgresql-client

# Copie o restante do código
COPY . .

# Comando para iniciar o aplicativo
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]