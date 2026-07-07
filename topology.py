from mininet.net import Mininet
from mininet.node import Node
from mininet.node import OVSSKernelSwitch
from mininet.link import TCLink
from mininet.log import setLogLevel


class LinuxRouter(Node):
    """
    Host Linux que atuará como firewall/roteador.
    """

    def config(self, **params):
        super().config(**params)

        # Habilita roteamento IPv4
        self.cmd("sysctl -w net.ipv4.ip_forward=1")

    def terminate(self):
        self.cmd("sysctl -w net.ipv4.ip_forward=0")
        super().terminate()


class FirewallTopology:

    def __init__(self):

       self.net = Mininet(
    controller=None,
    switch=OVSSKernelSwitch,
    link=TCLink,
    autoSetMacs=True,
    autoStaticArp=True
)
    def build(self):

        print("\n=== Criando switches ===")

        s_wan = self.net.addSwitch(
    "s1",
    dpid="0000000000000001",
    failMode="standalone"
)

        s_lan = self.net.addSwitch(
    "s2",
    dpid="0000000000000002",
    failMode="standalone"
)

        internet = self.net.addHost(
            "internet",
            ip="192.168.100.2/24",
            defaultRoute="via 192.168.100.1"
        )

        firewall = self.net.addHost(
            "fw",
            cls=LinuxRouter
        )

        web = self.net.addHost(
            "web",
            ip="10.0.0.10/24",
            defaultRoute="via 10.0.0.1"
        )

        dns = self.net.addHost(
            "dns",
            ip="10.0.0.20/24",
            defaultRoute="via 10.0.0.1"
        )

        admin = self.net.addHost(
            "admin",
            ip="10.0.0.100/24",
            defaultRoute="via 10.0.0.1"
        )

        client = self.net.addHost(
            "client",
            ip="10.0.0.101/24",
            defaultRoute="via 10.0.0.1"
        )

        print("\n=== Criando enlaces ===")

        self.net.addLink(internet, s_wan)

        self.net.addLink(firewall, s_wan, intfName1="fw-eth0")

        self.net.addLink(firewall, s_lan, intfName1="fw-eth1")

        self.net.addLink(web, s_lan)

        self.net.addLink(dns, s_lan)

        self.net.addLink(admin, s_lan)

        self.net.addLink(client, s_lan)

        print("\n=== Inicializando rede ===")

        self.net.start()

        print("\n=== Configurando interfaces do firewall ===")

        firewall.cmd("ifconfig fw-eth0 192.168.100.1/24")

        firewall.cmd("ifconfig fw-eth1 10.0.0.1/24")

        print("\n=== Limpando regras antigas ===")

        firewall.cmd("iptables -F")
        firewall.cmd("iptables -t nat -F")
        firewall.cmd("iptables -X")

        print("\n=== Topologia criada com sucesso ===")

        return self.net

    def stop(self):

        print("\n=== Encerrando rede ===")

        self.net.stop()


def create_network():
    topology = FirewallTopology()
    return topology.build()


if __name__ == "__main__":

    setLogLevel("info")

    topology = FirewallTopology()

    net = topology.build()

    print("\nTopologia criada com sucesso.")

    print("\nHosts disponíveis:")

    for host in net.hosts:
        print(f" - {host.name}: {host.IP()}")

    print("\nEntre no CLI do Mininet utilizando outro script (main.py) ou adapte este arquivo para testes.")

    topology.stop()