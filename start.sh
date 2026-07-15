#!/bin/bash
# Instala dependências básicas caso faltem
apt-get update && apt-get install -y wget unzip

# Descarrega o Xray se ainda não existir
if [ ! -f xray_exec ]; then
    wget -O xray_core.zip https://github.com/XTLS/Xray-core/releases/latest/download/xray-linux-64.zip
    unzip xray_core.zip xray
    mv xray xray_exec
    chmod +x xray_exec
fi

# Inicia o Xray em segundo plano e depois inicia o seu bot
./xray_exec -c xray/config.json &
python3 bot.py

