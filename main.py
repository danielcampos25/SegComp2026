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



        # -------------------------------
        # Firewall
        # -------------------------------


        setup_firewall(net)



        time.sleep(2)



        # -------------------------------
        # Testes automáticos
        # -------------------------------


        run_tests(net)



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