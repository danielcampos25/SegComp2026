from pathlib import Path


class ServerManager:
    """
    Responsável por iniciar os serviços utilizados durante os testes.
    """

    def __init__(self, net):

        self.net = net

        self.web = net.get("web")
        self.dns = net.get("dns")

    # ----------------------------------------------------
    # HTTPS
    # ----------------------------------------------------

    def start_https(self):

        cert_dir = Path("/tmp/certs")

        self.web.cmd(f"mkdir -p {cert_dir}")

        self.web.cmd(
            f"""
            openssl req -x509 -nodes \
            -days 365 \
            -newkey rsa:2048 \
            -keyout {cert_dir}/server.key \
            -out {cert_dir}/server.crt \
            -subj "/CN=web"
            """
        )

        self.web.cmd(
            f"""
            openssl s_server \
            -accept 443 \
            -cert {cert_dir}/server.crt \
            -key {cert_dir}/server.key \
            -www > /tmp/https.log 2>&1 &
            """
        )

        print("[+] HTTPS iniciado")

    # ----------------------------------------------------
    # DNS
    # ----------------------------------------------------

    def start_dns(self):

        self.dns.cmd(
            """
            dnsmasq \
            --no-daemon \
            --port=53 \
            > /tmp/dns.log 2>&1 &
            """
        )

        print("[+] DNS iniciado")

    # ----------------------------------------------------
    # FTP
    # ----------------------------------------------------

    def start_ftp(self):

        self.web.cmd(
            """
            python3 -m pyftpdlib \
            -p 21 \
            > /tmp/ftp.log 2>&1 &
            """
        )

        print("[+] FTP iniciado")

    # ----------------------------------------------------
    # Telnet
    # ----------------------------------------------------

    def start_telnet(self):

        self.web.cmd(
            """
            busybox telnetd \
            -p 23
            """
        )

        print("[+] Telnet iniciado")

    # ----------------------------------------------------
    # SSH
    # ----------------------------------------------------

    def start_ssh(self):

        self.web.cmd(
            """
            /usr/sbin/sshd
            """
        )

        print("[+] SSH iniciado")

    # ----------------------------------------------------
    # Inicialização completa
    # ----------------------------------------------------

    def start_all(self):

        print("\n=== Inicializando Serviços ===\n")

        self.start_https()
        self.start_dns()
        self.start_ftp()
        self.start_telnet()
        self.start_ssh()

        print("\n=== Serviços iniciados ===\n")