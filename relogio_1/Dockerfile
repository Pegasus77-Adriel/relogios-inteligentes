# Use uma imagem base do Python
FROM python:3.11.4-slim

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie os arquivos necessários para o diretório de trabalho no contêiner
COPY requirements.txt .

# Instale as dependências do seu projeto
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 12346
EXPOSE 12347
EXPOSE 12348
# Copie todo o código para o contêiner
COPY . .

# Comando padrão para executar sua aplicação
CMD ["python","relogio.py"]
