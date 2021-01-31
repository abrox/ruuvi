#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import logging
from collector import Collector
import json

logger = logging.getLogger(__name__)

sToLogLevel = {'debug': logging.DEBUG,
               'info': logging.INFO,
               'warning': logging.WARNING,
               'error': logging.ERROR
               }


class S(SimpleHTTPRequestHandler):

    def do_GET(self):  # pylint: disable=C0103

        path = self.path

        if path == '/ruuvi/all':
            c = Collector.getClient()
            latest = c.get_latest()
            values = []
            for key, value in latest.items():
                values.append(value)
            d = {'values': values}
            json_data = json.dumps(d)
            self.set_rsp_header(len(json_data))

            self.wfile.write(json_data.encode('utf-8'))

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])   # <--- Gets the size of data
        post_data = self.rfile.read(content_length)   # <--- Gets the data itself
        path = self.path
        logger.info(post_data.decode('utf-8'))

        if path == '/ruuvi/sensor':
            c = Collector.getClient()
            reguest_json = json.loads(post_data.decode('utf-8'))
            id = reguest_json['id']
            try:
                data = c.get_sensor_latest(id)
                json_data = json.dumps(data)
                self.set_rsp_header(len(json_data))
                self.wfile.write(json_data.encode('utf-8'))
            except KeyError:
                self.send_response(409)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

        elif path == '/ruuvi/loglevel':
            c = Collector.getClient()
            reguest_json = json.loads(post_data.decode('utf-8'))
            try:
                level = reguest_json['level']
                # Map to correct, trow KeyError if something else
                c.set_loglevel(sToLogLevel[level])
                logger.setLevel(sToLogLevel[level])
                json_data = "{\"level\":\"daa\"}"
                self.set_rsp_header(len(json_data))
                self.wfile.write(json_data.encode('utf-8'))
            except KeyError:
                self.send_response(409)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

    def set_rsp_header(self, data_len):
        """ Utility to create rsp header for messages."""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        #self.send_header('Content-Transfer-Encoding', 'UTF-8')
        self.send_header('Content-Length', data_len)
        self.end_headers()


def run(server_class=ThreadingHTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logger.info('Starting httpd...\n')
    try:
        Collector.CreateCollector()
        c = Collector.getClient()
        c.start()
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logger.info('Stopping httpd...\n')


if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
