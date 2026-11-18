from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path


class StockFixture(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/products.json":
            self.send_error(404)
            return
        if self.server.fail_next_request:
            self.server.fail_next_request = False
            self.send_error(503)
            return
        body = (Path(__file__).parent / "fixtures" / "products.json").read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main():
    with HTTPServer(("127.0.0.1", 8000), StockFixture) as server:
        server.fail_next_request = True
        print("Stock fixture at http://127.0.0.1:8000/products.json", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
