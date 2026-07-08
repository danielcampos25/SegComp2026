"""
servers.py

Gerenciamento dos serviços da rede.

Este módulo é responsável por iniciar e encerrar todos os serviços
executados nos hosts da topologia Mininet.

Serviços implementados:

- HTTPS
- DNS
- SSH
- FTP
- Telnet

Todos os serviços herdam da classe BaseServer.
"""

from pathlib import Path
from typing import Dict
from datetime import datetime
import time


# ============================================================
# Diretórios utilizados pelo projeto
# ============================================================

PROJECT_ROOT = Path(".")

WWW_DIRECTORY = PROJECT_ROOT / "www"

FTP_DIRECTORY = PROJECT_ROOT / "ftp"

DNS_DIRECTORY = PROJECT_ROOT / "dns"

LOG_DIRECTORY = PROJECT_ROOT / "reports_logs"

CERT_DIRECTORY = PROJECT_ROOT / "certificates"


# ============================================================
# Classe BaseServer
# ============================================================

class BaseServer:
    """
    Classe base para todos os serviços.

    Cada serviço conhece apenas o host onde está sendo executado.

    Toda lógica comum fica aqui para evitar duplicação.
    """

    def __init__(self, host, service_name):

        self.host = host

        self.service_name = service_name

        self.pid = None

        self.running = False

    # --------------------------------------------------------

    def start(self):
        """
        Deve ser implementado pelas subclasses.
        """
        raise NotImplementedError

    # --------------------------------------------------------

    def stop(self):

        if self.pid is not None:

            self.host.cmd(f"kill {self.pid}")

            self.pid = None

        self.running = False

    # --------------------------------------------------------

    def is_running(self):

        return self.running

    # --------------------------------------------------------

    def execute(self, command):
        """
        Executa um comando dentro do host Mininet.
        """

        return self.host.cmd(command)

    # --------------------------------------------------------

    def execute_background(self, command):
        """
        Executa um comando em background.

        O PID do processo é armazenado para encerramento futuro.
        """

        output = self.host.cmd(f"{command} > /dev/null 2>&1 & echo $!")

        self.pid = output.strip()

        self.running = True

    # --------------------------------------------------------

    def log(self, message):

        print(f"[{self.service_name}] {message}")


# ============================================================
# Gerenciador de processos
# ============================================================

class ProcessManager:
    """
    Mantém referência para todos os serviços iniciados.

    Isso facilita parar todos ao final do projeto.
    """

    def __init__(self):

        self.services: Dict[str, BaseServer] = {}

    # --------------------------------------------------------

    def register(self, server: BaseServer):

        self.services[server.service_name] = server

    # --------------------------------------------------------

    def start_all(self):

        print("\n===================================")
        print("Inicializando serviços")
        print("===================================\n")

        for server in self.services.values():

            server.log("Inicializando...")

            server.start()

            time.sleep(0.5)

        print("\nTodos os serviços foram iniciados.\n")

    # --------------------------------------------------------

    def stop_all(self):

        print("\n===================================")
        print("Encerrando serviços")
        print("===================================\n")

        for server in self.services.values():

            server.stop()

        print("\nTodos os serviços foram encerrados.\n")


# ============================================================
# Utilidades
# ============================================================

def create_directories():
    """
    Cria automaticamente todos os diretórios utilizados
    durante a execução.
    """

    WWW_DIRECTORY.mkdir(exist_ok=True)

    FTP_DIRECTORY.mkdir(exist_ok=True)

    DNS_DIRECTORY.mkdir(exist_ok=True)

    LOG_DIRECTORY.mkdir(exist_ok=True)


# ============================================================
# Página HTML utilizada pelo servidor HTTPS
# ============================================================

DEFAULT_HTML = """
<!DOCTYPE html>

<html>

<head>

<title>Projeto Segurança Computacional</title>

</head>

<body>

<h1>Servidor HTTPS</h1>

<p>
Projeto de Firewall utilizando Mininet e iptables.
</p>

</body>

</html>
"""


def create_default_page():

    page = WWW_DIRECTORY / "index.html"

    if page.exists():

        return

    page.write_text(DEFAULT_HTML)


# ============================================================
# Configuração do DNS
# ============================================================

DEFAULT_DNSMASQ = """
port=53

no-daemon

log-queries

address=/web.local/10.0.0.10

address=/dns.local/10.0.0.20
"""


def create_dns_configuration():

    conf = DNS_DIRECTORY / "dnsmasq.conf"

    if conf.exists():

        return

    conf.write_text(DEFAULT_DNSMASQ)


# ============================================================
# Diretório FTP
# ============================================================

def create_ftp_directory():

    readme = FTP_DIRECTORY / "README.txt"

    if readme.exists():

        return

    readme.write_text(
        "Servidor FTP do projeto de Segurança Computacional.\n"
    )

# ============================================================
# HTTPS Server
# ============================================================

class HTTPSServer(BaseServer):
    """
    Servidor HTTPS executado no host WEB.

    Utiliza um pequeno servidor Python com SSL.
    """

    def __init__(self, host):

        super().__init__(host, "HTTPS")

    def create_https_script(self):

        script = WWW_DIRECTORY / "https_server.py"

        script.unlink(missing_ok=True)

        script.write_text(
'''
import os, sys, ssl
from http.server import HTTPServer, SimpleHTTPRequestHandler

os.chdir("www")

try:
    httpd = HTTPServer(("0.0.0.0", 443), SimpleHTTPRequestHandler)
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(
        "../certificates/server.crt",
        "../certificates/server.key"
    )
    httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
    print("HTTPS Server iniciado.")
    sys.stdout.flush()
    httpd.serve_forever()
except Exception as e:
    print(f"HTTPS ERROR: {e}", file=sys.stderr)
    sys.stderr.flush()
'''
        )

    # --------------------------------------------------------

    def start(self):

        self.log("Preparando servidor HTTPS...")

        create_default_page()

        self.create_https_script()

        self.execute_background(
            "python3 www/https_server.py 2>>reports_logs/https_errors.log"
        )

        self.log("Servidor HTTPS iniciado.")


# ============================================================
# DNS Server
# ============================================================

class DNSServer(BaseServer):
    """
    Servidor DNS utilizando dnsmasq.
    """

    def __init__(self, host):

        super().__init__(host, "DNS")

    def start(self):

        self.log("Criando configuração DNS...")

        create_dns_configuration()

        self.execute_background(

            "dnsmasq "
            "--conf-file=dns/dnsmasq.conf"

        )

        self.log("Servidor DNS iniciado.")

# ============================================================
# FTP Server
# ============================================================

class FTPServer(BaseServer):
    """
    Servidor FTP utilizando pyftpdlib.
    """

    def __init__(self, host):

        super().__init__(host, "FTP")


    def create_ftp_script(self):

        script = FTP_DIRECTORY / "ftp_server.py"

        if script.exists():

            return


        script.write_text(
'''
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


authorizer = DummyAuthorizer()


authorizer.add_user(
    "ftpuser",
    "123456",
    "ftp",
    perm="elradfmw"
)


handler = FTPHandler

handler.authorizer = authorizer


server = FTPServer(
    ("0.0.0.0", 21),
    handler
)


print("FTP Server iniciado.")

server.serve_forever()
'''
        )


    def start(self):

        self.log("Preparando servidor FTP...")

        create_ftp_directory()

        self.create_ftp_script()


        self.execute_background(

            "python3 ftp/ftp_server.py"

        )


        self.log("Servidor FTP iniciado.")




# ============================================================
# SSH Server
# ============================================================

class SSHServer(BaseServer):
    """
    Servidor SSH utilizando OpenSSH.
    """

    def __init__(self, host):

        super().__init__(host, "SSH")


    def start(self):

        self.log("Iniciando SSH...")


        self.execute("mkdir -p /run/sshd")

        self.execute("ssh-keygen -A 2>>reports_logs/ssh_errors.log")


        self.execute_background(

            "/usr/sbin/sshd -D 2>>reports_logs/ssh_errors.log"

        )


        self.log("Servidor SSH iniciado.")




# ============================================================
# Telnet Server
# ============================================================

class TelnetServer(BaseServer):
    """
    Servidor Telnet.
    """

    def __init__(self, host):

        super().__init__(host, "TELNET")


    def start(self):

        self.log("Iniciando Telnet...")


        self.execute_background(

            "/usr/sbin/telnetd -F"

        )


        self.log("Servidor Telnet iniciado.")

# ============================================================
# Server Manager
# ============================================================


class ServerManager:
    """
    Controlador principal dos serviços.
    """


    def __init__(self, network):

        self.network = network

        self.process_manager = ProcessManager()


    def setup(self):

        create_directories()


        web = self.network.get("web")

        dns = self.network.get("dns")


        self.process_manager.register(

            HTTPSServer(web)

        )


        self.process_manager.register(

            FTPServer(web)

        )


        self.process_manager.register(

            SSHServer(web)

        )


        self.process_manager.register(

            TelnetServer(web)

        )


        self.process_manager.register(

            DNSServer(dns)

        )


    def start(self):

        self.setup()

        self.process_manager.start_all()



    def log_service_ports(self):

        ports = [
            ("HTTPS",  "web", "10.0.0.10", 443,  "TCP"),
            ("FTP",    "web", "10.0.0.10", 21,   "TCP"),
            ("SSH",    "web", "10.0.0.10", 22,   "TCP"),
            ("Telnet", "web", "10.0.0.10", 23,   "TCP"),
            ("DNS",    "dns", "10.0.0.20", 53,   "UDP/TCP"),
        ]

        path = LOG_DIRECTORY / "service_ports.log"
        with open(path, "w") as f:
            f.write("# Registro de Serviços e Portas\n")
            f.write(f"# Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"{'Serviço':<10} {'Host':<8} {'IP':<16} {'Porta':<8} {'Proto':<10}\n")
            f.write("-" * 52 + "\n")
            for name, host, ip, port, proto in ports:
                status = "RUNNING" if self.process_manager.services.get(name) and self.process_manager.services[name].is_running() else "STOPPED"
                f.write(f"{name:<10} {host:<8} {ip:<16} {port:<8} {proto:<10} {status}\n")

        print(f"[Log] Portas registradas em {path}")

    def stop(self):

        self.process_manager.stop_all()