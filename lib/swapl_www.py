# -----------------------------------------------------------------------------
# swapl_www.py
# -----------------------------------------------------------------------------

import http.server
import socketserver
import pathlib
import threading
import json
import os
import io
import sys

from urllib.parse import urlparse


class SWAPLHttpRequestHandler(http.server.SimpleHTTPRequestHandler):

    program = None

    def __init__(self, request, client_address, server):
        root_path = pathlib.Path(__file__).parent.resolve()
        self.root_path = str(root_path) + '/www/'
        os.chdir(self.root_path)
        super().__init__(request, client_address, server)

    def do_GET(self):
        parsed = urlparse(self.path)
        #print(self.path, parsed)
        if parsed.path == "/agentlist":
            alist = [ ]
            for agent in SWAPLHttpRequestHandler.program.get_agents().values():
                a_name = agent.get_field('name')
                a_role = agent.get_field('role')
                alist.append( agent.get_field('object').fields() )
                #{ 'name' : a_name,
                #                'role' : a_role } )
            content = json.dumps(alist)
            self.send_json(content)
        elif parsed.path == "/agent":
            agent = SWAPLHttpRequestHandler.program.get_agent(parsed.query)
            content = json.dumps(agent.get_field('object').fields())
            self.send_json(content)
        else:
            super().do_GET()

    def send_json(self, _json):
        #print(_json)
        enc = sys.getfilesystemencoding()
        encoded = _json.encode(enc, 'surrogateescape')
        f = io.BytesIO()
        f.write(encoded)
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        try:
            self.copyfile(f, self.wfile)
        finally:
            f.close()


# -----------------------------------------------------------------------------
class SWAPLHttpServer(threading.Thread):

    def __init__(self, port):
        super().__init__()
        self.port = port
        self.setDaemon(False)

    def run(self):
        Handler = SWAPLHttpRequestHandler
        socketserver.TCPServer.allow_reuse_address = True
        httpd = socketserver.TCPServer(("", self.port), Handler)
        httpd.serve_forever()
