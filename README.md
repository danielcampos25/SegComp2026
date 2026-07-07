# Projeto de Firewall - Segurança Computacional

## Descrição

Este projeto tem como objetivo implementar uma política de segurança utilizando um firewall baseado em **iptables** em uma rede simulada com o **Mininet**, conforme proposto na Parte V do projeto da disciplina de Segurança Computacional.

A rede simula um ambiente corporativo contendo serviços internos, um firewall e um host representando a Internet.

---

# Estrutura do Projeto

```
SegComp2026/
│
├── topology.py          # Criação da topologia da rede
├── firewall.py          # Configuração das regras do firewall
├── servers.py           # Inicialização dos serviços
├── tests.py             # Execução dos testes
├── certificates.py      # Geração de certificados e chaves
├── main.py              # Execução completa do projeto
│
├── certificates/        # Certificados HTTPS e chaves SSH
│
├── reports_logs/        # Logs dos testes
│
└── README.md
```

---

# Arquitetura da Rede

```
                    INTERNET
                       |
                 192.168.100.0/24
                       |
                  internet host
                 192.168.100.2
                       |
                  Switch WAN
                       |
                fw-eth0 (WAN)
              192.168.100.1
              +------------+
              | FIREWALL   |
              +------------+
              10.0.0.1
               fw-eth1 (LAN)
                       |
                  Switch LAN
      ---------------------------------------
      |          |          |               |
     web        dns       admin          client
 10.0.0.10   10.0.0.20  10.0.0.100   10.0.0.101
```

Todo o tráfego entre a Internet e a rede interna passa obrigatoriamente pelo firewall.

---

# Requisitos

O projeto foi desenvolvido para execução em:

- Ubuntu 24.04 (WSL2 ou Máquina Virtual)
- Python 3.13+
- Mininet
- Open vSwitch

Não é suportada execução diretamente no Windows.

---

# Instalação

Após clonar o repositório, entre na pasta do projeto:

```bash
cd SegComp2026
```

Conceda permissão de execução aos scripts:

```bash
chmod +x setup.sh
chmod +x run.sh
```

Execute o script de configuração:

```bash
./setup.sh
```

O script realiza automaticamente:

- Atualização dos pacotes do sistema;
- Instalação de todas as dependências do projeto;
- Criação do ambiente virtual Python (`.venv`);
- Instalação das bibliotecas Python necessárias;
- Criação das pastas `certificates/` e `reports_logs/`;
- Limpeza de configurações antigas do Mininet;
- Verificação da instalação das principais ferramentas.

Ao final da execução, o ambiente estará pronto para utilização.

---

# Executando o Projeto

Após concluir a instalação, basta executar:

```bash
./run.sh
```

O script realiza automaticamente:

- Ativação do ambiente virtual Python;
- Execução do projeto utilizando privilégios de administrador.

Não é necessário ativar manualmente o ambiente virtual nem utilizar diretamente o comando `python`.

---

# Caso seja necessário executar manualmente

Ative o ambiente virtual:

```bash
source .venv/bin/activate
```

Execute o projeto:

```bash
sudo -E python3 main.py
```
# Scripts Auxiliares

O projeto possui dois scripts para facilitar sua utilização.

| Script | Função |
|---------|--------|
| `setup.sh` | Configura todo o ambiente do projeto automaticamente. |
| `run.sh` | Executa o projeto com todas as configurações necessárias. |

Fluxo recomendado:

```bash
git clone <repositorio>

cd SegComp2026

chmod +x setup.sh run.sh

./setup.sh

./run.sh
```

# Serviços Implementados

O projeto disponibiliza os seguintes serviços:

- HTTPS
- DNS
- SSH
- FTP
- Telnet

O firewall será responsável por permitir ou bloquear esses serviços conforme a política de segurança definida.

---

# Política de Segurança

### Serviços Permitidos

- HTTPS
- DNS

### Serviços Restritos

- FTP
- Telnet

### Serviço Administrativo

- SSH apenas para o host administrador

---

# Fluxo de Execução

```
main.py
    │
    ├── topology.py
    │
    ├── certificates.py
    │
    ├── servers.py
    │
    ├── firewall.py
    │
    └── tests.py
```

---

# Testes Realizados

## Permitidos

- HTTPS
- DNS
- SSH (Administrador)

## Bloqueados

- FTP
- Telnet
- SSH (Cliente comum)

---

# Logs

Todos os logs produzidos pelo projeto serão armazenados na pasta:

```
reports_logs/
```

Exemplos:

```
https.log
dns.log
ssh.log
ftp.log
telnet.log
iptables.log
tests.log
```

---

# Certificados

Os certificados HTTPS e as chaves SSH serão gerados automaticamente durante a execução do projeto.

Os arquivos serão armazenados em:

```
certificates/
```

---

# Observações

Caso ocorra algum erro durante a execução do Mininet, execute novamente:

```bash
sudo mn -c
```

Caso o ambiente virtual não esteja ativo:

```bash
source .venv/bin/activate
```

---

# Autores

Projeto desenvolvido para a disciplina de Segurança Computacional.