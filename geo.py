from http.server import BaseHTTPRequestHandler, HTTPServer
import geoip2.database
from urllib.parse import urlparse, parse_qs

DATABASE_PATH = 'GeoLite2-Country.mmdb'
reader = geoip2.database.Reader(DATABASE_PATH)


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse query parameters
        query_components = parse_qs(urlparse(self.path).query)
        test_ip = query_components.get("ip", [self.client_address[0]])[0]

        try:
            response = reader.country(test_ip)
            print("test ip is" , test_ip)
            iso_code = response.country.iso_code
        except geoip2.errors.AddressNotFoundError:
            iso_code = "Unknown"

        print(f"Connection from {test_ip} - Country ISO code: {iso_code}")
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(f"Hello! The country code for IP {test_ip} is: {iso_code}", "utf-8"))


def run_server():
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, RequestHandler)
    print("Server started on port 8080...")
    httpd.serve_forever()


try:
    run_server()
except KeyboardInterrupt:
    pass
finally:
    reader.close()
    print("Server stopped.")
