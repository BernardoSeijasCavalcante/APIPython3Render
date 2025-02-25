#!/bin/bash

# Atualiza os pacotes e instala dependências
apt-get update && apt-get install -y curl gnupg2

# Adiciona a chave do repositório da Microsoft
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -

# Adiciona o repositório do SQL Server ODBC Driver
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Atualiza novamente os pacotes
apt-get update

# Instala o driver ODBC 18 para SQL Server e o gerenciador unixODBC
ACCEPT_EULA=Y apt-get install -y msodbcsql18 unixodbc-dev

# Instala as dependências do Python
pip install --upgrade pip
pip install -r requirements.txt