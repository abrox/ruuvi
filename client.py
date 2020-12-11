#!/usr/bin/env python3
import json
import urllib.request
import urllib.error
import logging
import calendar
from datetime import datetime


def to_unix_timestamp(time_str=datetime.utcnow().isoformat()):
    '''
     Convert date time to Unix timestamp
     Expect following format:yyyy-mm-dd hh:mm:ss e.g.2020-01-04 20:53:00
    '''
    dt = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%f")

    return int(calendar.timegm(dt.timetuple()))


def ruuvi_to_influx_line(data, excludes=['mac']):

    line = "ruuvi,"
    line += "id=\"{id}\" ".format(id=data['id'])
    values = data['data']
    for key in values:
        if key not in excludes:
            line += "{k}={v},".format(k=key, v=values[key])
    line = line[:-1]
    line = "{l} {t}".format(l=line, t=to_unix_timestamp(data['timestamp']))
    return line


def multiline_to_influx(data):
    sensors = data['values']
    lines = ""
    for sensor in sensors:
        line = ruuvi_to_influx_line(sensor)
        lines += "{l}\n".format(l=line)
    return lines


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
        HTTP_page = urllib.request.urlopen(url, timeout=5.0)
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
        multiline_to_influx(data)

"""
    ok, data = get_latest_single_sensor(ip=ip, id='C7:41:2E:60:DB:EC')
    if ok:
        print(data)
        line = ruuvi_to_influx_line(data)
        print(line)
"""
