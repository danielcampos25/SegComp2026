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

## Status atual do projeto

### ✅ Implementado

#### Estrutura base
- [x] Organização dos arquivos Python
- [x] .gitignore

#### Topologia de rede
- [x] Criação dos switches WAN/LAN
- [x] Criação do firewall Linux
- [x] Criação dos hosts: internet, web, dns, admin, client
- [x] Configuração das interfaces fw-eth0 e fw-eth1

#### Serviços
- [x] HTTPS
- [x] FTP
- [x] SSH
- [x] Telnet
- [x] DNS

#### Certificados HTTPS
- [x] Geração de certificado autoassinado
- [x] Validação de existência

#### Firewall (iptables)
- [x] Regras FORWARD no host fw (controle WAN ↔ LAN)
- [x] Regras INPUT no host web (controle local de serviços)
- [x] Regras INPUT no host dns (controle DNS)
- [x] Snapshot das regras em reports_logs/

#### Testes de Validação
- [x] HTTPS (internet → web): PASS
- [x] DNS (internet → dns): PASS
- [x] SSH Admin (admin → web): PASS
- [x] Telnet Bloqueado (client → web): PASS
- [x] FTP Bloqueado (client → web): PASS
- [x] SSH Cliente Bloqueado (client → web): PASS

#### Evidências
- [x] Log de testes (reports_logs/tests.log)
- [x] Snapshot das regras iptables (reports_logs/iptables_*.rules)

### 📝 Pendente

- [ ] Documentar ACLs Packet Tracer (Atividade 5.3)
- [ ] Avaliação dos Resultados (Atividade 5.5)
- [ ] Revisar README
- [ ] Preparar evidências finais para relatório

---

## Matriz de Regras (Firewall)

### Política Permitida
| Origem | Destino | Serviço | Porto | Ação |
|--------|---------|---------|-------|------|
| Internet (192.168.100.2) | Web Server (10.0.0.10) | HTTPS | 443/TCP | Permitir |
| Internet (192.168.100.2) | DNS Server (10.0.0.20) | DNS | 53/UDP | Permitir |
| Admin (10.0.0.100) | Servidores | SSH | 22/TCP | Permitir |

### Política Bloqueada
| Origem | Destino | Serviço | Porto | Ação |
|--------|---------|---------|-------|------|
| Qualquer | Servidores | Telnet | 23/TCP | Negar |
| Qualquer | Servidores | FTP | 21/TCP | Negar |
| Cliente comum (10.0.0.101) | Servidores | SSH | 22/TCP | Negar |
| WAN → LAN | Qualquer | Qualquer | — | Negar (default) |

---

## Portas dos Serviços

| Serviço | Host | Porto | Protocolo |
|---------|------|-------|-----------|
| HTTPS | web (10.0.0.10) | 443 | TCP |
| FTP | web (10.0.0.10) | 21 | TCP |
| SSH | web (10.0.0.10) | 22 | TCP |
| Telnet | web (10.0.0.10) | 23 | TCP |
| DNS | dns (10.0.0.20) | 53 | UDP/TCP |

---

## Como executar

Instalar dependências:

```bash
# CachyOS / Arch Linux (AUR)
yay -S mininet openvswitch python-pyftpdlib
yay -S openssl openssh dnsmasq inetutils dnsutils curl netcat-openbsd

# Ubuntu / Debian
sudo apt update
sudo apt install mininet openvswitch-switch python3-pip python3-venv
```

Executar:

```bash
sudo systemctl start ovsdb-server ovs-vswitchd
sudo mn -c
./run.sh
```
