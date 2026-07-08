# ACLs no Packet Tracer — Atividade 5.3

## Topologia Equivalente no Packet Tracer

```
[Internet] -- [Router/Firewall] -- [Switch] -- [Web Server]
                                               |-- [DNS Server]
                                               |-- [Admin PC]
                                               |-- [Client PC]
```

- **Internet**: 192.168.100.2/24
- **Router (FW)**: Fa0/0 = 192.168.100.1/24, Fa0/1 = 10.0.0.1/24
- **Web Server**: 10.0.0.10/24 (HTTPS, FTP, SSH, Telnet)
- **DNS Server**: 10.0.0.20/24 (DNS)
- **Admin**: 10.0.0.100/24
- **Client**: 10.0.0.101/24

---

## Extended ACL (100) — Controle de Acesso WAN → LAN

Aplicada na interface Fa0/0 (WAN) do roteador, **inbound**:

```
! --- Permitir HTTPS da Internet para o Web Server ---
access-list 100 permit tcp host 192.168.100.2 host 10.0.0.10 eq 443

! --- Permitir DNS da Internet para o DNS Server ---
access-list 100 permit udp host 192.168.100.2 host 10.0.0.20 eq 53

! --- Bloquear Telnet vindo da Internet ---
access-list 100 deny tcp 192.168.100.0 0.0.0.255 10.0.0.0 0.0.0.255 eq 23

! --- Bloquear FTP vindo da Internet ---
access-list 100 deny tcp 192.168.100.0 0.0.0.255 10.0.0.0 0.0.0.255 eq 21

! --- Bloquear SSH vindo da Internet ---
access-list 100 deny tcp 192.168.100.0 0.0.0.255 10.0.0.0 0.0.0.255 eq 22

! --- Negar todo o resto da Internet para a LAN ---
access-list 100 deny ip any 10.0.0.0 0.0.0.255
```

```
! Aplicar ACL na interface WAN (entrada)
interface fa0/0
 ip access-group 100 in
```

---

## Extended ACL (101) — Controle de Acesso Interno (LAN)

Aplicada na interface Fa0/1 (LAN) do roteador, **inbound**, para controlar tráfego entre hosts da LAN:

```
! --- SSH apenas do Admin ---
access-list 101 permit tcp host 10.0.0.100 10.0.0.0 0.0.0.255 eq 22

! --- Bloquear Telnet de qualquer origem interna ---
access-list 101 deny tcp any 10.0.0.0 0.0.0.255 eq 23

! --- Bloquear FTP de qualquer origem interna ---
access-list 101 deny tcp any 10.0.0.0 0.0.0.255 eq 21

! --- Bloquear SSH do Cliente Comum ---
access-list 101 deny tcp host 10.0.0.101 10.0.0.0 0.0.0.255 eq 22

! --- Permitir HTTPS e DNS internos ---
access-list 101 permit tcp any host 10.0.0.10 eq 443
access-list 101 permit udp any host 10.0.0.20 eq 53

! --- Permitir o restante do tráfego interno ---
access-list 101 permit ip any any
```

```
! Aplicar ACL na interface LAN (entrada)
interface fa0/1
 ip access-group 101 in
```

> **Nota:** No Packet Tracer, as ACLs estendidas devem ser aplicadas o mais próximo possível da origem do tráfego. A ACL 100 na WAN filtra tráfego externo; a ACL 101 na LAN filtra tráfego entre hosts internos.

---

## Equivalência com iptables (implementado no projeto)

| Regra | iptables | ACL Packet Tracer |
|-------|----------|-------------------|
| Internet → Web: HTTPS | `iptables -A FORWARD -s 192.168.100.2 -d 10.0.0.10 -p tcp --dport 443 -j ACCEPT` | `permit tcp host 192.168.100.2 host 10.0.0.10 eq 443` |
| Internet → DNS: DNS | `iptables -A FORWARD -s 192.168.100.2 -d 10.0.0.20 -p udp --dport 53 -j ACCEPT` | `permit udp host 192.168.100.2 host 10.0.0.20 eq 53` |
| Admin → Web: SSH | `iptables -A INPUT -s 10.0.0.100 -p tcp --dport 22 -j ACCEPT` | `permit tcp host 10.0.0.100 10.0.0.0 0.0.0.255 eq 22` |
| Bloquear Telnet | `iptables -A INPUT -p tcp --dport 23 -j DROP` | `deny tcp any 10.0.0.0 0.0.0.255 eq 23` |
| Bloquear FTP | `iptables -A INPUT -p tcp --dport 21 -j DROP` | `deny tcp any 10.0.0.0 0.0.0.255 eq 21` |
| Bloquear SSH (client) | `iptables -A INPUT -s 10.0.0.101 -p tcp --dport 22 -j DROP` | `deny tcp host 10.0.0.101 10.0.0.0 0.0.0.255 eq 22` |
| Default DROP | `iptables -P FORWARD DROP` | `deny ip any 10.0.0.0 0.0.0.255` |
