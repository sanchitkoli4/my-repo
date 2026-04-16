#!/usr/bin/env python3
"""
Simple dev server for this repo.
Run: python serve.py [port]
Opens http://localhost:<port>/index.html in your default browser.
"""
import http.server
import socketserver
import webbrowser
import sys
import os

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000

# Ensure we serve from the repo directory where this file lives
HERE = os.path.dirname(os.path.abspath(__file__)) or os.getcwd()
os.chdir(HERE)

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    url = f"http://localhost:{PORT}/index.html"
    print(f"Serving {HERE} at {url}")
    try:
        webbrowser.open(url)
    except Exception:
        pass
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.server_close()
