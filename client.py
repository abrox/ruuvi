#!/usr/bin/env python3
import json
from validate import validate_json
import urllib.request
import urllib.error

schema_file = './schema/ruuvi.json'


def get_from_server(ip='127.0.0.1', port=8080, path='/ruuvi/all'):
    url = "http://{ip}:{po}{pa}".format(ip=ip, po=port, pa=path)
    try:
        HTTP_page = urllib.request.urlopen(url, timeout=5.0)
        data = HTTP_page.read()
        json_data = json.loads(data)
        is_valid, msg = validate_json(json_data, schema_file)
        print(json_data, is_valid, msg)
    except urllib.error.URLError as e:
        print("Failed to fetch:", e)


def post_to_server(id, ip='127.0.0.1', port=8080, path='/ruuvi/sensor'):
    url = "http://{ip}:{po}{pa}".format(ip=ip, po=port, pa=path)
    d = {'id': id}
    params = json.dumps(d).encode('utf8')
    try:
        req = urllib.request.Request(url,
                                     data=params,
                                     headers={'content-type': 'application/json'})
        response = urllib.request.urlopen(req, timeout=5.0)
        data = response.read()
        json_data = json.loads(data)
        is_valid, msg = validate_json(json_data, schema_file)
        print(json_data, is_valid, msg)
    except urllib.error.URLError as e:
        print("Failed to fetch:", e)


if __name__ == '__main__':
    #  url = 'http://192.168.66.36:8080/sensor'
    url = 'http://127.0.0.1:8080/ruuvi/all'
    # get_from_server(url)
    post_to_server(id='123')
