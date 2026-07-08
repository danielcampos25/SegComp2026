"""
tests.py

Testes de validação do firewall.

Executa testes nos serviços permitidos e bloqueados,
registrando todas as evidências em reports_logs/.
"""

import os
from datetime import datetime


LOG_DIR = "reports_logs"


class TestManager:

    def __init__(self, network):

        self.net = network

        self.internet = network.get("internet")
        self.web = network.get("web")
        self.dns = network.get("dns")
        self.admin = network.get("admin")
        self.client = network.get("client")

        self.results = []
        self.log_file = os.path.join(LOG_DIR, "tests.log")

    def run_all(self):

        print("Iniciando testes de validação do firewall...\n")

        os.makedirs(LOG_DIR, exist_ok=True)

        self._write_log("# Testes de Validação - Firewall")
        self._write_log(f"# Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        self._test_https()
        self._test_dns()
        self._test_ssh_admin()
        self._test_telnet_blocked()
        self._test_ftp_blocked()
        self._test_ssh_client_blocked()

        self._print_summary()
        self._write_summary()

    def _write_log(self, text):

        with open(self.log_file, "a") as f:
            f.write(text + "\n")

    def _log_result(self, test_name, command, output, passed):

        status = "PASS" if passed else "FAIL"
        timestamp = datetime.now().strftime("%H:%M:%S")
        line = (
            f"[{timestamp}] {test_name}: {status}\n"
            f"  Comando: {command}\n"
            f"  Saída:   {output.strip()}\n"
        )
        print(line)
        self._write_log(line)
        self.results.append((test_name, passed))

    def _test_https(self):

        name = "HTTPS (internet -> web)"
        cmd = "timeout 10 curl -k -s -o /dev/null -w '%{http_code}' https://10.0.0.10/ 2>&1"
        output = self.internet.cmd(cmd)
        passed = "200" in output
        self._log_result(name, cmd, output, passed)

    def _test_dns(self):

        name = "DNS (internet -> dns)"
        cmd = "timeout 5 nslookup web.local 10.0.0.20 2>&1"
        output = self.internet.cmd(cmd)
        passed = "Name:" in output and "web.local" in output and "10.0.0.10" in output
        self._log_result(name, cmd, output, passed)

    def _test_ssh_admin(self):

        name = "SSH Admin (admin -> web)"
        cmd = (
            "python3 -c "
            "\"import socket; s=socket.socket();"
            " s.settimeout(3); s.connect(('10.0.0.10', 22));"
            " s.close(); print('OK')\" 2>&1"
        )
        output = self.admin.cmd(cmd)
        passed = "OK" in output
        self._log_result(name, cmd, output, passed)

    def _test_telnet_blocked(self):

        name = "Telnet Bloqueado (client -> web)"
        cmd = "timeout 5 telnet 10.0.0.10 23 2>&1 || true"
        output = self.client.cmd(cmd)
        passed = (
            "Unable to connect" in output
            or "Connection refused" in output
            or "No route to host" in output
            or "timed out" in output
            or output.strip() == ""
            or (output.strip().startswith("Trying") and "Connected" not in output)
        )
        self._log_result(name, cmd, output, passed)

    def _test_ftp_blocked(self):

        name = "FTP Bloqueado (client -> web)"
        cmd = "timeout 5 curl -s ftp://10.0.0.10/ 2>&1"
        output = self.client.cmd(cmd)

        passed = (
            "Failed" in output
            or "failed" in output
            or "refused" in output
            or "timed out" in output
            or "Could not" in output
            or output.strip() == ""
        )
        self._log_result(name, cmd, output, passed)

    def _test_ssh_client_blocked(self):

        name = "SSH Cliente Bloqueado (client -> web)"
        cmd = (
            "timeout 7 python3 -c "
            "\"import socket; s=socket.socket();"
            " s.settimeout(5); s.connect(('10.0.0.10', 22))\" 2>&1"
        )
        output = self.client.cmd(cmd)
        passed = "timed out" in output
        self._log_result(name, cmd, output, passed)

    def _print_summary(self):

        print("===================================")
        print(" Resumo dos Testes")
        print("===================================")

        for name, passed in self.results:
            status = "✓ PASS" if passed else "✗ FAIL"
            print(f"  {status} - {name}")

        total = len(self.results)
        passed_count = sum(1 for _, p in self.results if p)
        print(f"\n{passed_count}/{total} testes passaram.")

    def _write_summary(self):

        self._write_log("\n" + "=" * 40)
        self._write_log("RESUMO FINAL")
        self._write_log("=" * 40)

        for name, passed in self.results:
            status = "PASS" if passed else "FAIL"
            self._write_log(f"  [{status}] {name}")

        total = len(self.results)
        passed_count = sum(1 for _, p in self.results if p)
        self._write_log(f"\n{passed_count}/{total} testes passaram.")
        self._write_log(f"Concluído em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
