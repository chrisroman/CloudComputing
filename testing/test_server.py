from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
  # GET
  def do_POST(self):
    self.send_response(200)
    self.send_header('Content-type','text/html')
    self.end_headers()


def run():
  print('starting server...')
  # Server settings
  # Choose port 8080, for port 80, which is normally used for a http server, you need root access
  server_address = ('127.0.0.1', 8081)
  httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
  print('running server...')
  httpd.serve_forever()

run()
