# Controle de Desenvolvimento — Projeto Segurança Computacional 2026

## ✅ Projeto Completo

### Topologia de Rede (`topology.py`)
- [x] Switches WAN (s1) e LAN (s2) com OVS
- [x] Hosts: internet, fw, web, dns, admin, client
- [x] Firewall Linux com ip_forward e iptables
- [x] Interfaces fw-eth0 (WAN) e fw-eth1 (LAN)

### Certificados HTTPS (`certificates.py`)
- [x] Geração de certificado autoassinado com OpenSSL
- [x] Validação de existência (não recria se já existe)

### Serviços (`servers.py`)
- [x] HTTPS (443) no host web
- [x] FTP (21) no host web
- [x] SSH (22) no host web
- [x] Telnet (23) no host web
- [x] DNS (53) no host dns
- [x] Registro de portas em `reports_logs/service_ports.log`

### Firewall (`firewall.py`) — iptables
- [x] FORWARD no host fw: controle WAN ↔ LAN
- [x] INPUT no host web: HTTPS (qualquer), SSH (admin), bloqueio Telnet/FTP/SSH-client
- [x] INPUT no host dns: DNS (qualquer)
- [x] Default DROP em todas as chains
- [x] LOG de pacotes bloqueados
- [x] Snapshot em `reports_logs/iptables_*.rules`
- [x] Limpeza automática ao encerrar

### Testes (`tests.py`) — 6/6 passando
- [x] HTTPS (internet → web): PASS
- [x] DNS (internet → dns): PASS
- [x] SSH Admin (admin → web): PASS
- [x] Telnet Bloqueado (client → web): PASS
- [x] FTP Bloqueado (client → web): PASS
- [x] SSH Cliente Bloqueado (client → web): PASS

### Logs e Evidências
- [x] `reports_logs/tests.log` — resultados detalhados
- [x] `reports_logs/service_ports.log` — portas dos serviços
- [x] `reports_logs/iptables_*.rules` — snapshots das regras
- [x] `reports_logs/evidencias_completas.log` — relatório consolidado
- [x] `reports_logs/https_errors.log` — erros do servidor HTTPS
- [x] `reports_logs/ssh_errors.log` — erros do servidor SSH
- [x] Logs limpos a cada execução (sem acúmulo)

### Documentação
- [x] `README.md` — documentação completa do projeto
- [x] `packet_tracer_acls.md` — ACLs Cisco Packet Tracer (Atividade 5.3)
- [x] Avaliação dos Resultados (Atividade 5.5) em `evidencias_completas.log`

---

## Matriz de Regras

### Permitido
| Origem | Destino | Serviço | Porto | Ação | Onde |
|--------|---------|---------|-------|------|------|
| Internet (192.168.100.2) | Web (10.0.0.10) | HTTPS | 443/TCP | ACCEPT | fw FORWARD |
| Internet (192.168.100.2) | DNS (10.0.0.20) | DNS | 53/UDP | ACCEPT | fw FORWARD |
| Admin (10.0.0.100) | Web (10.0.0.10) | SSH | 22/TCP | ACCEPT | web INPUT |

### Bloqueado
| Origem | Destino | Serviço | Porto | Ação | Onde |
|--------|---------|---------|-------|------|------|
| Qualquer | Web | Telnet | 23/TCP | LOG + DROP | web INPUT + fw FORWARD |
| Qualquer | Web | FTP | 21/TCP | LOG + DROP | web INPUT + fw FORWARD |
| WAN (192.168.100.0/24) | LAN (10.0.0.0/24) | SSH | 22/TCP | LOG + DROP | fw FORWARD |
| Client (10.0.0.101) | Web | SSH | 22/TCP | LOG + DROP | web INPUT |
| WAN → LAN | Qualquer | Qualquer | — | DROP (default) | fw FORWARD |

---

## Estrutura Final

```
SegComp2026/
├── main.py                 # Orquestrador
├── topology.py             # Topologia Mininet
├── firewall.py             # Regras iptables
├── servers.py              # Serviços de rede
├── tests.py                # Testes de validação
├── certificates.py         # Certificados HTTPS
├── packet_tracer_acls.md   # ACLs Packet Tracer
├── TODO.md                 # Este arquivo
├── README.md               # Documentação
├── setup.sh                # Instalação (Ubuntu)
├── run.sh                  # Execução
├── certificates/           # Certificados gerados
└── www/                    # Páginas e scripts dos servidores
```
