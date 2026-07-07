from mininet.net import Mininet
from mininet.node import Node
from mininet.node import OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel


class LinuxRouter(Node):
    """
    Nó utilizado como firewall/roteador.
    O encaminhamento IP será habilitado durante a inicialização.
    """

    def config(self, **params):
        super().config(**params)
        self.cmd("sysctl -w net.ipv4.ip_forward=1")

    def terminate(self):
        self.cmd("sysctl -w net.ipv4.ip_forward=0")
        super().terminate()


def create_topology():

    net = Mininet(controller=None, switch=OVSKernelSwitch)

    print("*** Criando hosts")

    internet = net.addHost(
        "internet",
        ip="10.0.0.1/24",
        defaultRoute="via 10.0.0.254"
    )

    web = net.addHost(
        "web",
        ip="10.0.0.10/24",
        defaultRoute="via 10.0.0.254"
    )

    dns = net.addHost(
        "dns",
        ip="10.0.0.20/24",
        defaultRoute="via 10.0.0.254"
    )

    admin = net.addHost(
        "admin",
        ip="10.0.0.100/24",
        defaultRoute="via 10.0.0.254"
    )

    client = net.addHost(
        "client",
        ip="10.0.0.101/24",
        defaultRoute="via 10.0.0.254"
    )

    firewall = net.addHost(
        "fw",
        cls=LinuxRouter,
        ip="10.0.0.254/24"
    )

    print("*** Criando switch")

    s1 = net.addSwitch("s1")

    print("*** Conectando hosts")

    net.addLink(internet, s1)
    net.addLink(web, s1)
    net.addLink(dns, s1)
    net.addLink(admin, s1)
    net.addLink(client, s1)
    net.addLink(firewall, s1)

    print("*** Inicializando rede")

    net.start()

    print("*** Topologia criada com sucesso")

    return net


if __name__ == "__main__":

    setLogLevel("info")

    net = create_topology()

    CLI(net)

    net.stop()