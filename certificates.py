"""
certificates.py

Responsável pela geração automática dos certificados utilizados
pelo servidor HTTPS.

Caso os certificados já existam, nenhuma ação é realizada.
"""

from pathlib import Path
import subprocess


class CertificateManager:

    def __init__(self):

        self.cert_dir = Path("certificates")

        self.cert_file = self.cert_dir / "server.crt"

        self.key_file = self.cert_dir / "server.key"

    def create_directory(self):
        """
        Cria o diretório certificates caso não exista.
        """

        self.cert_dir.mkdir(exist_ok=True)

    def certificates_exist(self):
        """
        Verifica se os certificados já existem.
        """

        return self.cert_file.exists() and self.key_file.exists()

    def generate(self):
        """
        Gera um certificado autoassinado utilizando OpenSSL.
        """

        self.create_directory()

        if self.certificates_exist():

            print("[Certificates] Certificados encontrados.")

            return

        print("[Certificates] Gerando certificados HTTPS...")

        command = [
            "openssl",
            "req",
            "-x509",
            "-newkey",
            "rsa:2048",
            "-nodes",
            "-days",
            "365",
            "-keyout",
            str(self.key_file),
            "-out",
            str(self.cert_file),
            "-subj",
            "/C=BR/ST=DistritoFederal/L=Brasilia/O=SegComp/OU=Firewall/CN=web.local"
        ]

        subprocess.run(command, check=True)

        print("[Certificates] Certificados criados com sucesso.")

    def get_certificate(self):

        return str(self.cert_file)

    def get_private_key(self):

        return str(self.key_file)


if __name__ == "__main__":

    manager = CertificateManager()

    manager.generate()

    print()

    print("Certificado:", manager.get_certificate())

    print("Chave:", manager.get_private_key())