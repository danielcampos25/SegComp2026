
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
