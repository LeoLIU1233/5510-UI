"""Local preview launcher for the Harbor Invest UI prototype."""

from __future__ import annotations

import argparse
import threading
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


ROOT = Path(__file__).resolve().parent
HOST = "127.0.0.1"
PREFERRED_PORT = 5510

class PreviewHandler(SimpleHTTPRequestHandler):
    """Serve the prototype without cached files during iterative preview."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, max-age=0")
        super().end_headers()

    def log_message(self, message_format, *args):
        print(f"[UI] {message_format % args}")


def create_server():
    last_error = None
    for port in range(PREFERRED_PORT, PREFERRED_PORT + 20):
        try:
            return ThreadingHTTPServer((HOST, port), PreviewHandler), port
        except OSError as error:
            last_error = error
    raise RuntimeError("No available local port was found.") from last_error


def main():
    parser = argparse.ArgumentParser(description="Run the local UI prototype.")
    parser.add_argument("--no-browser", action="store_true", help="Do not open a browser automatically.")
    args = parser.parse_args()

    server, port = create_server()
    url = f"http://{HOST}:{port}/index.html"

    if not args.no_browser:
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()

    print("")
    print("Harbor Invest UI preview is running.")
    print(f"Open: {url}")
    print("Press Ctrl+C to stop the server.")
    print("")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping preview server...")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
