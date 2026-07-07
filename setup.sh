#!/bin/bash

############################################################
# Projeto de Firewall - Segurança Computacional
#
# Script de configuração automática do ambiente
#
############################################################

set -e

echo "========================================="
echo " Projeto Firewall - Setup"
echo "========================================="
echo

# ----------------------------------------------------------
# Verifica Ubuntu
# ----------------------------------------------------------

if ! command -v apt >/dev/null 2>&1; then
    echo "Este script deve ser executado em uma distribuição baseada em Ubuntu."
    exit 1
fi

# ----------------------------------------------------------
# Atualização
# ----------------------------------------------------------

echo "[1/8] Atualizando pacotes..."

sudo apt update

# ----------------------------------------------------------
# Dependências
# ----------------------------------------------------------

echo
echo "[2/8] Instalando dependências..."

sudo apt install -y \
python3 \
python3-pip \
python3-venv \
python3-full \
mininet \
openvswitch-switch \
iptables \
openssl \
openssh-server \
dnsmasq \
inetutils-telnetd \
telnet \
dnsutils \
curl \
netcat-openbsd \
tree

# ----------------------------------------------------------
# Ambiente virtual
# ----------------------------------------------------------

echo
echo "[3/8] Configurando ambiente virtual..."

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

source .venv/bin/activate

# ----------------------------------------------------------
# Pacotes Python
# ----------------------------------------------------------

echo
echo "[4/8] Instalando dependências Python..."

pip install --upgrade pip

pip install pyftpdlib

# ----------------------------------------------------------
# Estrutura do projeto
# ----------------------------------------------------------

echo
echo "[5/8] Criando diretórios..."

mkdir -p certificates
mkdir -p reports_logs

# ----------------------------------------------------------
# Limpeza do Mininet
# ----------------------------------------------------------

echo
echo "[6/8] Limpando topologias antigas..."

sudo mn -c >/dev/null 2>&1 || true

# ----------------------------------------------------------
# Verificação
# ----------------------------------------------------------

echo
echo "[7/8] Verificando instalação..."

echo

python3 --version

echo

echo "Mininet:"
mn --version

echo

echo "OpenSSL:"
openssl version

echo

echo "DNSMasq:"
dnsmasq --version | head -n 1

echo

echo "iptables:"
iptables --version

echo

echo "pyftpdlib:"
python -m pyftpdlib --help >/dev/null && echo "OK"

# ----------------------------------------------------------
# Finalização
# ----------------------------------------------------------

echo
echo "[8/8] Finalizado!"
echo

echo "========================================="
echo " Ambiente configurado com sucesso!"
echo "========================================="
echo

echo "Para executar o projeto:"

echo

echo "source .venv/bin/activate"
echo "sudo -E python3 main.py"

echo