from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse as urlparse


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        query = urlparse.parse_qs(parsed_path.query)
        if 'code' in query:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(
                b'Authorization successful. You can close this window.')
            self.server.auth_code = query['code'][0]
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Authorization code not found.')


def run_server():
    server_address = ('', 8888)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print('Waiting for authorization...')
    httpd.handle_request()
    return httpd.auth_code


if __name__ == "__main__":
    auth_code = run_server()
    print(f'Authorization Code: {auth_code}')
