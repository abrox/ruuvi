#!/usr/bin/env python3
from ruuvitag_sensor.ruuvi import RuuviTagSensor
import threading
import time
import datetime
import copy


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
        self.lock = threading.RLock()
        threading.Timer(1, self.update_availability).start()

    def update_availability(self):
        delete = []
        with self.lock:
            for key, val in self.data.items():
                data = val['data']
                data['availability'] -= 1

                if data['availability'] <= 0:
                    delete.append(key)

            for i in delete:
                del self.data[i]
        threading.Timer(1, self.update_availability).start()

    def get_latest(self):
        """Get lates measurements.
        Returns:
            Dictonary having latest measurements of the sensors.
            Sensor MAC address is a key and value is dictonary containing
            having timestamp, id and data. data is dictonary contain measured
            values from sensor.
        """
        with self.lock:
            data = copy.deepcopy(self.data)
        return data

    def get_sensor_latest(self, id):
        """Latest measurements of single sensor.
        Args:
            id:
                MAC address of the sensor.
        Returns:
            latest mesurment reseived from the sensor.
        Throws:
            KeyError in case id requested is not in a list.
        """
        with self.lock:
            data = copy.deepcopy(self.data[id])
        return data

    def handle_data(self, found_data):
        data = found_data[1]
        data['availability'] = 10
        item = {'id': found_data[0],
                'data': data,
                'timestamp': datetime.datetime.utcnow().isoformat(),
                }
        with self.lock:
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
