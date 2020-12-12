#!/usr/bin/env python3
import json
import urllib.request
import urllib.error
import logging


def get_latest_all_sensors(ip, port=8080, path='/ruuvi/all'):
    """Latest measurements from all available sensors.
    Returns:
        tuple (rc , data)
            When OK:
                rc:True data having latest mesurments.
            When Fail:
                rc:False, data is none
    """
    rc = (False, None)
    url = "http://{ip}:{po}{pa}".format(ip=ip, po=port, pa=path)
    try:
        HTTP_page = urllib.request.urlopen(url, timeout=5)
        data = HTTP_page.read()
        json_data = json.loads(data)
        rc = (True, json_data)
    except urllib.error.URLError as e:
        logging.warning("Failed to fetch:", e)
    return rc


def get_latest_single_sensor(id, ip, port=8080, path='/ruuvi/sensor'):
    """Latest measurements from single sensor.
    args:
        id:
            MAC address of the sensor.
    Returns:
        tuple (rc , data)
            When OK:
                rc:True data having latest mesurments.
            When Fail:
                rc:False, data is none
    """
    url = "http://{ip}:{po}{pa}".format(ip=ip, po=port, pa=path)
    d = {'id': id}
    params = json.dumps(d).encode('utf8')
    rc = (False, None)
    try:
        req = urllib.request.Request(url,
                                     data=params,
                                     headers={'content-type': 'application/json'})
        response = urllib.request.urlopen(req, timeout=5.0)
        data = response.read()
        json_data = json.loads(data)
        rc = (True, json_data)
    except urllib.error.URLError as e:
        logging.warning("Failed to fetch:", e)
    return rc


if __name__ == '__main__':
    ip = '192.168.66.6'

    ok, data = get_latest_all_sensors(ip=ip)
    if ok:
        print(data)
    else:
        print("Failed")

    ok, data = get_latest_single_sensor(ip=ip, id='C7:41:2E:60:DB:EC')
    if ok:
        print(data)
    else:
        print("Failed")
