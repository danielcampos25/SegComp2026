# Controle de Desenvolvimento
## Projeto Segurança Computacional 2026


## Visão geral

Este projeto tem como objetivo implementar uma política de segurança
utilizando Mininet, serviços reais e regras de firewall.

A arquitetura simulada representa uma empresa contendo:

- Rede externa (Internet);
- Firewall Linux utilizando iptables;
- Rede interna;
- Servidores;
- Clientes;
- Usuários administrativos.


---

# Status atual do projeto


## ✅ Implementado


### Estrutura base

- [x] Organização dos arquivos Python
- [x] README inicial
- [x] .gitignore


### Topologia de rede

Arquivo:
topology.py

Status:

🟡 Parcialmente concluído


Implementado:

- [x] Criação dos switches WAN/LAN
- [x] Criação do firewall Linux
- [x] Criação dos hosts:
    - internet
    - web
    - dns
    - admin
    - client

- [x] Configuração das interfaces:
    - fw-eth0
    - fw-eth1

Pendências:

- [ ] Corrigir comunicação entre hosts
- [ ] Validar funcionamento do switch OVS
- [ ] Validar pingall


---

# Serviços


Arquivo:
servers.py


Status:

✅ Implementado


Serviços criados:

- [x] HTTPS
- [x] FTP
- [x] SSH
- [x] Telnet
- [x] DNS


Pendências:

- [ ] Validar comunicação após firewall
- [ ] Registrar portas utilizadas
- [ ] Gerar evidências para relatório


---

# Certificados HTTPS


Arquivo:
certificates.py


Status:

✅ Implementado


Funções:

- [x] Geração de certificado
- [x] Validação de existência


Pendências:

- [ ] Documentar no relatório
- [ ] Associar certificado ao servidor HTTPS


---

# Firewall


Arquivo:
firewall.py


Status:

❌ Não implementado


Deve implementar:


## Política permitida

| Origem | Destino | Serviço | Ação |
|-|-|-|-|
| Internet | Web Server | HTTPS | Permitir |
| Internet | DNS Server | DNS | Permitir |
| Admin | Servidores | SSH | Permitir |


## Política bloqueada

| Origem | Destino | Serviço | Ação |
|-|-|-|-|
| Qualquer | Servidores | Telnet | Negar |
| Qualquer | Servidores | FTP | Negar |
| Cliente comum | Servidores | SSH | Negar |


Implementar usando:

- iptables


---

# Testes


Arquivo:
tests.py


Status:

❌ Não implementado


Deve implementar:


## Política permitida

| Origem | Destino | Serviço | Ação |
|-|-|-|-|
| Internet | Web Server | HTTPS | Permitir |
| Internet | DNS Server | DNS | Permitir |
| Admin | Servidores | SSH | Permitir |


## Política bloqueada

| Origem | Destino | Serviço | Ação |
|-|-|-|-|
| Qualquer | Servidores | Telnet | Negar |
| Qualquer | Servidores | FTP | Negar |
| Cliente comum | Servidores | SSH | Negar |


Implementar usando:

- iptables


---

# Testes


Arquivo:
main.py


Status:

🟡 Parcialmente concluído


Já executa:

- [x] Topologia
- [x] Certificados
- [x] Serviços


Aguardando:

- [ ] Firewall
- [ ] Testes automáticos


---

# Próximos passos recomendados


Ordem de implementação:


1. Corrigir comunicação Mininet:



4. Gerar logs automaticamente


5. Preparar evidências para relatório


6. Revisar README


---

# Como executar


Instalar dependências:


```bash
sudo apt update

sudo apt install \
mininet \
openvswitch-switch \
python3-pip \
python3-venv