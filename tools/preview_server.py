#!/usr/bin/env python3
"""
NEXUS OS - Design System Web Preview Server
Serves the interactive web showcase on port 8080 (or next free port).
"""

import http.server
import socketserver
import os
import sys

PORT = 8080
WEB_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "design-system", "web"))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

def run():
    os.chdir(WEB_DIR)
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"==========================================================")
        print(f" NEXUS OS — Design System Web Showcase Running            ")
        print(f" URL: http://localhost:{PORT}                              ")
        print(f" Press Ctrl+C to terminate server                         ")
        print(f"==========================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down preview server.")

if __name__ == "__main__":
    run()
