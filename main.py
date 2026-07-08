"""
main.py

Arquivo principal do projeto de Segurança Computacional.

Responsável por:

- Criar a topologia de rede;
- Gerenciar certificados;
- Inicializar servidores;
- Aplicar firewall;
- Executar testes;
- Encerrar o ambiente.

Execução:

sudo python3 main.py
"""


from mininet.cli import CLI
from mininet.log import setLogLevel


from topology import create_network


from servers import ServerManager


# Será implementado posteriormente
try:

    from firewall import FirewallManager

except ImportError:

    FirewallManager = None



# Será implementado posteriormente
try:

    from tests import TestManager

except ImportError:

    TestManager = None



# Certificados

try:

    from certificates import CertificateManager

except ImportError:

    CertificateManager = None



import os
import shutil
import time




# ============================================================
# Preparação dos certificados
# ============================================================


def setup_certificates():

    print("\n==============================")
    print(" Preparando certificados ")
    print("==============================\n")


    if CertificateManager is None:

        print(
            "[AVISO] certificates.py ainda não implementado."
        )

        return


    manager = CertificateManager()

    manager.generate()






# ============================================================
# Inicialização dos servidores
# ============================================================


def setup_servers(net):

    print("\n==============================")
    print(" Inicializando servidores ")
    print("==============================\n")


    servers = ServerManager(net)

    servers.start()


    return servers






# ============================================================
# Configuração do firewall
# ============================================================


def setup_firewall(net):


    print("\n==============================")
    print(" Configurando firewall ")
    print("==============================\n")



    if FirewallManager is None:

        print(
            "[AVISO] firewall.py ainda não implementado."
        )

        return None



    firewall = FirewallManager(net)

    firewall.apply_rules()


    return firewall






# ============================================================
# Geração de evidências
# ============================================================


def generate_evidence(servers):

    print("\n==============================")
    print(" Gerando evidências ")
    print("==============================\n")

    import os
    from datetime import datetime

    log_dir = "reports_logs"
    os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    evidence_file = os.path.join(log_dir, "evidencias_completas.log")

    with open(evidence_file, "w") as f:
        f.write("=" * 60 + "\n")
        f.write(" RELATÓRIO DE EVIDÊNCIAS - FIREWALL\n")
        f.write(f" Gerado em: {timestamp}\n")
        f.write("=" * 60 + "\n\n")

        f.write("1. TOPOLOGIA DE REDE\n")
        f.write("-" * 40 + "\n")
        f.write("""
            WAN: 192.168.100.0/24
              internet: 192.168.100.2
              fw-eth0:  192.168.100.1

            LAN: 10.0.0.0/24
              fw-eth1: 10.0.0.1
              web:     10.0.0.10  (HTTPS, FTP, SSH, Telnet)
              dns:     10.0.0.20  (DNS)
              admin:   10.0.0.100
              client:  10.0.0.101
""")

        f.write("\n2. POLÍTICA DE SEGURANÇA\n")
        f.write("-" * 40 + "\n")
        f.write("""
   Serviços Permitidos:  HTTPS, DNS
   Serviços Restritos:   Telnet, FTP
   Serviço Admin:        SSH (apenas admin)
""")

        f.write("\n3. MATRIZ DE REGRAS (iptables)\n")
        f.write("-" * 40 + "\n")
        f.write("""
   PERMITIDO:
     Internet -> Web:  HTTPS (tcp/443)  [fw FORWARD]
     Internet -> DNS:  DNS (udp/53)     [fw FORWARD]
     Admin -> Web:     SSH (tcp/22)     [web INPUT]

   BLOQUEADO:
     Qualquer -> Web:  Telnet (tcp/23)  [web INPUT + fw FORWARD]
     Qualquer -> Web:  FTP (tcp/21)     [web INPUT + fw FORWARD]
     Client -> Web:    SSH (tcp/22)     [web INPUT]
     WAN -> LAN:       Qualquer         [fw FORWARD default DROP]
""")

        f.write("\n4. PORTAS DOS SERVIÇOS\n")
        f.write("-" * 40 + "\n")
        for name, host, ip, port, proto in [
            ("HTTPS", "web", "10.0.0.10", 443, "TCP"),
            ("FTP",   "web", "10.0.0.10", 21,  "TCP"),
            ("SSH",   "web", "10.0.0.10", 22,  "TCP"),
            ("Telnet","web", "10.0.0.10", 23,  "TCP"),
            ("DNS",   "dns", "10.0.0.20", 53,  "UDP/TCP"),
        ]:
            f.write(f"   {name:<8} {ip:<16} {port:<5} {proto:<8}\n")

        f.write("\n5. ARQUIVOS DE EVIDÊNCIA\n")
        f.write("-" * 40 + "\n")
        for file in sorted(os.listdir(log_dir)):
            f.write(f"   reports_logs/{file}\n")

        f.write("\n" + "=" * 60 + "\n")
        f.write(" AVALIAÇÃO DOS RESULTADOS (Atividade 5.5)\n")
        f.write("=" * 60 + "\n\n")

        f.write("1. O firewall protege contra invasões?\n")
        f.write("-" * 40 + "\n")
        f.write("""   Sim. O firewall implementa uma política de default DROP nas chains
   FORWARD e INPUT, bloqueando por padrão todo o tráfego não autorizado.
   Apenas conexões HTTPS (443/tcp) da Internet para o servidor web e
   consultas DNS (53/udp) da Internet para o servidor DNS são permitidas
   através do firewall. Qualquer tentativa de acesso externo a serviços
   como Telnet, FTP ou SSH é rejeitada silenciosamente (DROP), sem
   responder ao requisitante — o que torna a rede interna invisível para
   varreduras externas.\n\n""")

        f.write("2. O firewall protege contra malware interno?\n")
        f.write("-" * 40 + "\n")
        f.write("""   Parcialmente. O firewall controla o tráfego entre redes diferentes
   (WAN ↔ LAN), mas hosts no mesmo segmento LAN (10.0.0.0/24) comunicam-se
   diretamente via switch, sem passar pelo firewall. Para mitigar riscos
   internos, foram aplicadas regras iptables na chain INPUT dos próprios
   servidores (web e dns), restringindo serviços localmente. Apesar disso,
   um host comprometido na mesma VLAN ainda pode realizar ataques laterais
   (ARP spoofing, scans). A proteção completa contra malware interno
   exigiria segmentação de rede (VLANs/DMZ), firewall stateful por host
   (ex: nftables), e um sistema de detecção de intrusão (IDS).\n\n""")

        f.write("3. O firewall protege contra phishing?\n")
        f.write("-" * 40 + "\n")
        f.write("""   Indiretamente. Phishing é um ataque de engenharia social que explora
   o fator humano, não vulnerabilidades técnicas de rede. Um firewall não
   pode impedir que um usuário clique em um link malicioso ou forneça
   credenciais em um site fraudulento. No entanto, o firewall contribui
   para a defesa em profundidade ao:
     - Reduzir a superfície de ataque (apenas HTTPS e DNS são expostos);
     - Bloquear conexões de saída para portas não autorizadas;
     - Impedir que servidores internos sejam acessados por serviços
       inseguros como Telnet (tráfego em texto claro) e FTP.
   A mitigação de phishing requer camadas adicionais: filtro antispam,
   DMARC/DKIM, MVTs, conscientização de usuários e MFA.\n\n""")

        f.write("=" * 60 + "\n")
        f.write(" ACLs Packet Tracer (Atividade 5.3)\n")
        f.write("=" * 60 + "\n\n")
        f.write("""   As ACLs equivalentes para Cisco Packet Tracer estão documentadas no
   arquivo packet_tracer_acls.md na raiz do projeto.

   Resumo das ACLs:

   ACL 100 (WAN - interface Fa0/0 in):
     permit tcp host 192.168.100.2 host 10.0.0.10 eq 443
     permit udp host 192.168.100.2 host 10.0.0.20 eq 53
     deny tcp 192.168.100.0 0.0.0.255 10.0.0.0 0.0.0.255 eq 23
     deny tcp 192.168.100.0 0.0.0.255 10.0.0.0 0.0.0.255 eq 21
     deny tcp 192.168.100.0 0.0.0.255 10.0.0.0 0.0.0.255 eq 22
     deny ip any 10.0.0.0 0.0.0.255

   ACL 101 (LAN - interface Fa0/1 in):
     permit tcp host 10.0.0.100 10.0.0.0 0.0.0.255 eq 22
     deny tcp any 10.0.0.0 0.0.0.255 eq 23
     deny tcp any 10.0.0.0 0.0.0.255 eq 21
     deny tcp host 10.0.0.101 10.0.0.0 0.0.0.255 eq 22
     permit ip any any\n""")

    print(f"Evidências salvas em {evidence_file}")

    print("\nArquivos gerados em reports_logs/:")
    for file in sorted(os.listdir(log_dir)):
        print(f"  - {file}")


# ============================================================
# Execução dos testes
# ============================================================


def run_tests(net):


    print("\n==============================")
    print(" Executando testes ")
    print("==============================\n")



    if TestManager is None:

        print(
            "[AVISO] tests.py ainda não implementado."
        )

        return



    tester = TestManager(net)

    tester.run_all()






# ============================================================
# Programa principal
# ============================================================


def main():


    print("\n")
    print("====================================")
    print(" Projeto Segurança Computacional ")
    print(" Firewall + Mininet ")
    print("====================================")


    servers = None

    firewall = None

    if os.path.exists("reports_logs"):
        shutil.rmtree("reports_logs")
    os.makedirs("reports_logs", exist_ok=True)


    try:


        # -------------------------------
        # Criar rede
        # -------------------------------


        net = create_network()



        time.sleep(2)



        # -------------------------------
        # Certificados HTTPS
        # -------------------------------


        setup_certificates()



        # -------------------------------
        # Serviços
        # -------------------------------


        servers = setup_servers(net)



        time.sleep(3)

        servers.log_service_ports()



        # -------------------------------
        # Firewall
        # -------------------------------


        firewall = setup_firewall(net)



        time.sleep(2)



        # -------------------------------
        # Testes automáticos
        # -------------------------------


        run_tests(net)

        generate_evidence(servers)



        print("\n====================================")
        print(" Ambiente iniciado com sucesso ")
        print("====================================\n")



        print(
            "Use a CLI do Mininet para testes manuais."
        )


        CLI(net)




    except KeyboardInterrupt:


        print(
            "\nExecução interrompida pelo usuário."
        )



    finally:



        print(
            "\nEncerrando ambiente..."
        )



        if firewall:
            firewall.clear_rules()



        if servers:

            servers.stop()



        if 'net' in locals():

            net.stop()



        print(
            "Projeto finalizado."
        )






if __name__ == "__main__":


    setLogLevel("info")


    main()