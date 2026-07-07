
from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl
import os

os.chdir("www")

httpd = HTTPServer(("0.0.0.0", 443), SimpleHTTPRequestHandler)

ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

ctx.load_cert_chain(
    "certificates/server.crt",
    "certificates/server.key"
)

httpd.socket = ctx.wrap_socket(
    httpd.socket,
    server_side=True
)

print("HTTPS Server iniciado.")

httpd.serve_forever()
