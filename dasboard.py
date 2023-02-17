import http.server
import socketserver


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = 'index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)


# Create an object of the above class
handler_object = MyHttpRequestHandler

PORT = 8000
HOSTNAME = ""

my_server = socketserver.TCPServer((HOSTNAME, PORT), handler_object)

try:
    # Start the server
    my_server.serve_forever()
except KeyboardInterrupt:
    my_server.server_close()
    print("here")
