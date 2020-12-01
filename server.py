#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import SimpleHTTPRequestHandler, HTTPServer
import logging


class S(SimpleHTTPRequestHandler):

    def do_GET(self):  # pylint: disable=C0103

        path = self.path

        if path == '/sensor':
            file = open("./data/data.json", "r")
            data = file.read()

            self.set_rsp_header(len(data))

            self.wfile.write(data.encode('utf-8'))

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info(post_data.decode('utf-8'))

        #self._set_response()
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        file = open("../data/data.json", "r")
        data = file.read()

        self.set_rsp_header(len(data))

        self.wfile.write(data.encode('utf-8'))

    def set_rsp_header(self, data_len):
        """ Utility to create rsp header for messages."""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        #self.send_header('Content-Transfer-Encoding', 'UTF-8')
        self.send_header('Content-Length', data_len)
        self.end_headers()


def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
