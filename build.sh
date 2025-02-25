#!/bin/bash

# Atualiza os pacotes básicos e instala dependências do ODBC
apt-get update && apt-get install -y curl gnupg2 unixodbc unixodbc-dev

# Adiciona a chave do repositório da Microsoft
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -

# Detecta a versão do Ubuntu
UBUNTU_VERSION=$(lsb_release -rs)

# Adiciona o repositório correto para a versão do Ubuntu
if [ "$UBUNTU_VERSION" == "22.04" ]; then
    curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
else
    curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
fi

# Atualiza novamente os pacotes
apt-get update

# Aceita os termos da Microsoft e instala o ODBC Driver 18 para SQL Server
ACCEPT_EULA=Y apt-get install -y msodbcsql18

# Verifica se o driver foi instalado corretamente
odbcinst -q -d

# Instala as dependências do Python
pip install --upgrade pip
pip install -r requirements.txt
