"""
firewall.py

Configuração do firewall utilizando iptables.

Estratégia de defesa em profundidade:
  - Host firewall (fw): controla tráfego entre WAN e LAN via chain FORWARD
  - Host web: controla acesso local aos serviços (HTTPS, SSH, Telnet, FTP) via chain INPUT
  - Host dns: controla acesso local ao DNS via chain INPUT

Topologia:
  WAN: 192.168.100.0/24
    - internet: 192.168.100.2
    - fw-eth0:  192.168.100.1
  LAN: 10.0.0.0/24
    - fw-eth1: 10.0.0.1
    - web:     10.0.0.10
    - dns:     10.0.0.20
    - admin:   10.0.0.100
    - client:  10.0.0.101
"""

import os
from datetime import datetime


class FirewallManager:

    def __init__(self, network):

        self.net = network

        self.fw = network.get("fw")
        self.web = network.get("web")
        self.dns = network.get("dns")

    def apply_rules(self):

        print("\n=== Aplicando regras do firewall ===\n")

        for host in (self.fw, self.web, self.dns):
            self._flush_host(host)

        self._apply_fw_rules()
        self._apply_web_rules()
        self._apply_dns_rules()
        self._save_snapshot()

        print("Firewall configurado com sucesso.\n")

    def clear_rules(self):

        print("\n=== Removendo regras do firewall ===\n")

        for host in (self.fw, self.web, self.dns):
            self._flush_host(host)

    @staticmethod
    def _flush_host(host):

        host.cmd("iptables -F")
        host.cmd("iptables -X")
        host.cmd("iptables -t nat -F")
        host.cmd("iptables -P INPUT ACCEPT")
        host.cmd("iptables -P FORWARD ACCEPT")
        host.cmd("iptables -P OUTPUT ACCEPT")

    # ----------------------------------------------------------------
    # Regras no firewall (fw)
    # ----------------------------------------------------------------
    # A chain FORWARD controla o tráfego entre WAN (internet) e LAN.
    # A chain INPUT controla acesso ao próprio firewall.
    # ----------------------------------------------------------------

    def _apply_fw_rules(self):

        fw = self.fw

        # --- Default policies ---
        fw.cmd("iptables -P FORWARD DROP")
        fw.cmd("iptables -P INPUT DROP")
        fw.cmd("iptables -P OUTPUT ACCEPT")

        # --- INPUT chain ---
        fw.cmd("iptables -A INPUT -i lo -j ACCEPT")
        fw.cmd("iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT")
        fw.cmd("iptables -A INPUT -j LOG --log-prefix '[FW-INPUT-DROP] ' --log-level 4")

        # --- FORWARD chain ---
        fw.cmd("iptables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT")

        # Política Permitida:
        # 1. Internet → Web Server: HTTPS (tcp/443)
        fw.cmd(
            "iptables -A FORWARD "
            "-s 192.168.100.2 -d 10.0.0.10 "
            "-p tcp --dport 443 -j ACCEPT"
        )

        # 2. Internet → DNS Server: DNS (udp/53)
        fw.cmd(
            "iptables -A FORWARD "
            "-s 192.168.100.2 -d 10.0.0.20 "
            "-p udp --dport 53 -j ACCEPT"
        )

        # 3. Bloqueio explícito de serviços restritos vindo da WAN (log + drop)
        # Telnet (tcp/23)
        fw.cmd(
            "iptables -A FORWARD "
            "-s 192.168.100.0/24 -d 10.0.0.0/24 "
            "-p tcp --dport 23 "
            "-j LOG --log-prefix '[FW-FWD-BLOCK-TELNET] '"
        )
        fw.cmd(
            "iptables -A FORWARD "
            "-s 192.168.100.0/24 -d 10.0.0.0/24 "
            "-p tcp --dport 23 -j DROP"
        )
        # FTP (tcp/21)
        fw.cmd(
            "iptables -A FORWARD "
            "-s 192.168.100.0/24 -d 10.0.0.0/24 "
            "-p tcp --dport 21 "
            "-j LOG --log-prefix '[FW-FWD-BLOCK-FTP] '"
        )
        fw.cmd(
            "iptables -A FORWARD "
            "-s 192.168.100.0/24 -d 10.0.0.0/24 "
            "-p tcp --dport 21 -j DROP"
        )
        # SSH (tcp/22) vindo da WAN
        fw.cmd(
            "iptables -A FORWARD "
            "-s 192.168.100.0/24 -d 10.0.0.0/24 "
            "-p tcp --dport 22 "
            "-j LOG --log-prefix '[FW-FWD-BLOCK-SSH-WAN] '"
        )
        fw.cmd(
            "iptables -A FORWARD "
            "-s 192.168.100.0/24 -d 10.0.0.0/24 "
            "-p tcp --dport 22 -j DROP"
        )

        # Log de todo o tráfego FORWARD bloqueado
        fw.cmd(
            "iptables -A FORWARD "
            "-j LOG --log-prefix '[FW-FWD-DROP] ' --log-level 4"
        )

    # ----------------------------------------------------------------
    # Regras no servidor web
    # ----------------------------------------------------------------
    # Como admin e client estão na mesma LAN que web, o tráfego entre
    # eles NÃO passa pelo firewall. Por isso aplicamos regras locais
    # via INPUT chain no próprio host web.
    #
    # Serviços no web: HTTPS (443), SSH (22), FTP (21), Telnet (23)
    # ----------------------------------------------------------------

    def _apply_web_rules(self):

        web = self.web

        web.cmd("iptables -P INPUT DROP")
        web.cmd("iptables -P OUTPUT ACCEPT")

        web.cmd("iptables -A INPUT -i lo -j ACCEPT")
        web.cmd("iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT")

        # --- Política Permitida ---
        # HTTPS de qualquer origem (incluindo internet)
        web.cmd("iptables -A INPUT -p tcp --dport 443 -j ACCEPT")

        # SSH apenas do admin (10.0.0.100)
        web.cmd(
            "iptables -A INPUT "
            "-s 10.0.0.100 -p tcp --dport 22 -j ACCEPT"
        )

        # --- Política Bloqueada ---
        # Telnet (tcp/23) de qualquer origem
        web.cmd(
            "iptables -A INPUT "
            "-p tcp --dport 23 "
            "-j LOG --log-prefix '[WEB-BLOCK-TELNET] '"
        )
        web.cmd("iptables -A INPUT -p tcp --dport 23 -j DROP")

        # FTP (tcp/21) de qualquer origem
        web.cmd(
            "iptables -A INPUT "
            "-p tcp --dport 21 "
            "-j LOG --log-prefix '[WEB-BLOCK-FTP] '"
        )
        web.cmd("iptables -A INPUT -p tcp --dport 21 -j DROP")

        # SSH do client (10.0.0.101) explicitamente bloqueado
        web.cmd(
            "iptables -A INPUT "
            "-s 10.0.0.101 -p tcp --dport 22 "
            "-j LOG --log-prefix '[WEB-BLOCK-SSH-CLIENT] '"
        )
        web.cmd(
            "iptables -A INPUT "
            "-s 10.0.0.101 -p tcp --dport 22 -j DROP"
        )

    # ----------------------------------------------------------------
    # Regras no servidor DNS
    # ----------------------------------------------------------------

    def _apply_dns_rules(self):

        dns = self.dns

        dns.cmd("iptables -P INPUT DROP")
        dns.cmd("iptables -P OUTPUT ACCEPT")

        dns.cmd("iptables -A INPUT -i lo -j ACCEPT")
        dns.cmd("iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT")

        # DNS (udp+tcp 53) de qualquer origem
        dns.cmd("iptables -A INPUT -p udp --dport 53 -j ACCEPT")
        dns.cmd("iptables -A INPUT -p tcp --dport 53 -j ACCEPT")

    # ----------------------------------------------------------------
    # Snapshot das regras para evidências
    # ----------------------------------------------------------------

    def _save_snapshot(self):

        log_dir = "reports_logs"
        os.makedirs(log_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for name, host in (("fw", self.fw), ("web", self.web), ("dns", self.dns)):

            rules = host.cmd("iptables -L -v -n 2>&1")

            nat_rules = host.cmd("iptables -t nat -L -v -n 2>&1")

            path = os.path.join(log_dir, f"iptables_{name}.rules")

            with open(path, "w") as f:
                f.write(f"# Regras iptables do host {name}\n")
                f.write(f"# Gerado em: {timestamp}\n\n")
                f.write("# === FILTER TABLE ===\n")
                f.write(rules)
                f.write("\n\n# === NAT TABLE ===\n")
                f.write(nat_rules)
