# Projeto de Firewall - Segurança Computacional

## Descrição

Implementação de uma política de segurança utilizando firewall baseado em **iptables** em rede simulada com **Mininet**, conforme a Parte V da disciplina de Segurança Computacional.

A rede simula um ambiente corporativo: Internet, firewall Linux, servidores internos (web, dns), administrador e cliente comum.

---

## Estrutura do Projeto

```
SegComp2026/
├── main.py                 # Orquestrador principal
├── topology.py             # Topologia da rede (Mininet)
├── firewall.py             # Regras iptables (fw, web, dns)
├── servers.py              # Serviços: HTTPS, DNS, SSH, FTP, Telnet
├── tests.py                # Testes automáticos de validação
├── certificates.py         # Geração de certificados HTTPS
├── packet_tracer_acls.md   # ACLs equivalentes para Packet Tracer
├── TODO.md                 # Controle de desenvolvimento
├── setup.sh                # Script de instalação (Ubuntu)
├── run.sh                  # Script de execução
├── certificates/           # Certificados e chaves gerados
├── reports_logs/           # Logs e evidências (gerado na execução)
└── www/                    # Páginas HTML e script HTTPS
```

---

## Arquitetura da Rede

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

## Requisitos

- Linux (Ubuntu 24.04+ ou Arch/CachyOS)
- Python 3.13+
- Mininet
- Open vSwitch
- iptables
- OpenSSH, dnsmasq, OpenSSL, curl

---

## Instalação

### Ubuntu/Debian
```bash
./setup.sh
```

### CachyOS / Arch Linux (AUR)
```bash
yay -S mininet openvswitch python-pyftpdlib
yay -S openssl openssh dnsmasq inetutils dnsutils curl
```

---

## Execução

```bash
sudo systemctl start ovsdb-server ovs-vswitchd   # se necessário
sudo mn -c                                         # limpar topologias antigas
./run.sh                                           # executa o projeto
```

---

## Fluxo de Execução

```
main.py
  ├── topology.py       (cria rede, switches, hosts)
  ├── certificates.py   (gera certificados HTTPS)
  ├── servers.py        (inicia serviços nos hosts)
  ├── firewall.py       (aplica regras iptables)
  └── tests.py          (executa 6 testes de validação)
```

---

## Política de Segurança

### Serviços Permitidos
| Origem | Destino | Serviço | Porto | Ação |
|--------|---------|---------|-------|------|
| Internet (192.168.100.2) | Web Server (10.0.0.10) | HTTPS | 443/TCP | Permitir |
| Internet (192.168.100.2) | DNS Server (10.0.0.20) | DNS | 53/UDP | Permitir |
| Admin (10.0.0.100) | Servidores | SSH | 22/TCP | Permitir |

### Serviços Bloqueados
| Origem | Destino | Serviço | Porto | Ação |
|--------|---------|---------|-------|------|
| Qualquer | Servidores | Telnet | 23/TCP | Negar |
| Qualquer | Servidores | FTP | 21/TCP | Negar |
| Cliente (10.0.0.101) | Servidores | SSH | 22/TCP | Negar |
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

## Implementação do Firewall

### Host `fw` (iptables FORWARD — controle WAN ↔ LAN)
- Default policy: DROP
- Liberado: HTTPS (internet → web), DNS (internet → dns)
- Bloqueado com log: Telnet, FTP, SSH vindos da WAN

### Host `web` (iptables INPUT — controle local)
- Default policy: DROP
- Liberado: HTTPS (qualquer origem), SSH (admin 10.0.0.100)
- Bloqueado com log: Telnet, FTP, SSH do cliente

### Host `dns` (iptables INPUT — controle DNS)
- Default policy: DROP
- Liberado: DNS (UDP/TCP 53)

---

## Testes de Validação

6/6 testes passando:

| Teste | Comando | Resultado |
|-------|---------|-----------|
| HTTPS (internet → web) | `curl -k https://10.0.0.10/` | PASS (200) |
| DNS (internet → dns) | `nslookup web.local 10.0.0.20` | PASS |
| SSH Admin (admin → web) | `socket.connect(('10.0.0.10', 22))` | PASS |
| Telnet Bloqueado (client → web) | `telnet 10.0.0.10 23` | PASS (bloqueado) |
| FTP Bloqueado (client → web) | `curl ftp://10.0.0.10/` | PASS (bloqueado) |
| SSH Cliente Bloqueado (client → web) | `socket.connect(('10.0.0.10', 22))` | PASS (bloqueado) |

---

## Evidências Geradas

Após a execução, `reports_logs/` contém:

| Arquivo | Conteúdo |
|---------|----------|
| `tests.log` | Resultados detalhados de cada teste |
| `service_ports.log` | Portas e status dos serviços |
| `iptables_fw.rules` | Regras do firewall (host fw) |
| `iptables_web.rules` | Regras do servidor web |
| `iptables_dns.rules` | Regras do servidor DNS |
| `evidencias_completas.log` | Relatório consolidado com política, regras, testes e avaliação |

---

## ACLs Packet Tracer (Atividade 5.3)

Documentação completa em [`packet_tracer_acls.md`](packet_tracer_acls.md).

### Resumo
- **ACL 100** (interface WAN Fa0/0 in): filtra tráfego da Internet para a LAN
- **ACL 101** (interface LAN Fa0/1 in): filtra tráfego entre hosts internos

---

## Avaliação dos Resultados (Atividade 5.5)

### 1. O firewall protege contra invasões?
**Sim.** Default DROP nas chains FORWARD e INPUT. Apenas HTTPS e DNS são permitidos da Internet. O DROP silencioso torna a rede interna invisível para varreduras externas.

### 2. O firewall protege contra malware interno?
**Parcialmente.** Firewall controla tráfego entre redes (WAN ↔ LAN). Hosts na mesma LAN comunicam-se via switch, sem passar pelo firewall. Regras INPUT nos servidores mitigam riscos locais. Proteção completa exigiria VLANs/DMZ + IDS.

### 3. O firewall protege contra phishing?
**Indiretamente.** Firewall reduz superfície de ataque (apenas HTTPS e DNS expostos) e bloqueia serviços inseguros (Telten, FTP). Phishing é ataque de engenharia social e requer camadas adicionais: filtro antispam, DMARC, MFA e conscientização.

---

## Observações

```bash
# Limpar topologias antigas do Mininet
sudo mn -c

# Ativar ambiente virtual manualmente
source .venv/bin/activate
```

---

## Autores

Projeto desenvolvido para a disciplina de Segurança Computacional — 2026.
