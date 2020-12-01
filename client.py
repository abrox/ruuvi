#!/usr/bin/env python3
import json
from validate import validate_json
import urllib.request
import urllib.error

#url = 'http://192.168.66.36:8080/sensor'
url = 'http://127.0.0.1:8080/sensor'
schema_file = './schema/ruuvi.json'

try:
    HTTP_page = urllib.request.urlopen(url, timeout=5.0)
    data = HTTP_page.read()
    json_data = json.loads(data)
    is_valid, msg = validate_json(json_data, schema_file)
    print(json_data, is_valid, msg)
except urllib.error.URLError as e:
    print("Failed to fetch:", e)
