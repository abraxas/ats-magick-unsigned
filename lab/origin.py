#!/usr/bin/env python3
"""Serve a tiny PNG for the ATS magick unsigned-convert lab."""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

IMG_PATH = Path("/img.png")
LISTEN_HOST = "0.0.0.0"
LISTEN_PORT = 8080


class OriginHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def do_GET(self) -> None:
        body = IMG_PATH.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "image/png")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt: str, *args: object) -> None:
        del fmt, args


def main() -> int:
    if not IMG_PATH.is_file():
        raise SystemExit(f"missing {IMG_PATH}")
    server = ThreadingHTTPServer((LISTEN_HOST, LISTEN_PORT), OriginHandler)
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
