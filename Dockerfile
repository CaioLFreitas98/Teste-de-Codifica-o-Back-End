# Etapa de build
FROM python:3.10-slim

# Define diretório de trabalho
WORKDIR /code

# Copia os arquivos do projeto
COPY . .

# Instala as dependências
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Comando padrão
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
