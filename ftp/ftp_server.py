
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
