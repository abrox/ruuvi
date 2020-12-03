#!/usr/bin/env python3
from ruuvitag_sensor.ruuvi import RuuviTagSensor
import threading
import time
import datetime


class Collector(threading.Thread):

    _client = None

    @staticmethod
    def CreateCollector():
        Collector._client = Collector()

    @staticmethod
    def getClient():
        return Collector._client

    def __init__(self):
        threading.Thread.__init__(self)
        self.data = {}

    def get_latest(self):
        return self.data

    def handle_data(self, found_data):
        item = {'id': found_data[0],
                'data': found_data[1],
                'timestamp': datetime.datetime.utcnow().isoformat()
                }
        self.data[found_data[0]] = item

    def run(self):
        RuuviTagSensor.get_datas(self.handle_data)


class myThread (threading.Thread):
    def __init__(self, collector):
        threading.Thread.__init__(self)
        self.collector = collector

    def print_result(self):
        latest = self.collector.get_latest()
        print(latest)

    def run(self):
        while True:
            self.print_result()
            time.sleep(1)


if __name__ == '__main__':
    c = Collector()
    c.start()
    th = myThread(c)
    th.start()
