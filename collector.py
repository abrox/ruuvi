#!/usr/bin/env python3
from ruuvitag_sensor.ruuvi import RuuviTagSensor
import threading
import datetime
import copy
import logging

logger = logging.getLogger(__name__)


class Collector(threading.Thread):
    """ Ruuvi data collector.
    Read and collect data from sensors.
    Keep up latest values, and act as a proxy between
    ruuvi tags and web server.
    """
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
        logger.setLevel(logging.INFO)
        threading.Timer(1, self.update_availability).start()


    def set_loglevel(self,level):
        logger.setLevel(level)


    def update_availability(self):
        """ Sensor availability.
        Keep track about sensor availability by countting
        availability down with 1 sec timer.By following availability
        it is possible to track connection quality.
        """
        delete = []
        with self.lock:
            for key, val in self.data.items():
                data = val['data']
                data['availability'] -= 1

                if data['availability'] <= 0:
                    logger.warning(f"{key} Not available anymore")
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
        """Ruuvi callback.
        Store sensor data to dict for future use.
        """
        data = found_data[1]
        data['availability'] = 10
        item = {'id': found_data[0],
                'data': data,
                'timestamp': datetime.datetime.utcnow().isoformat(),
                }
        logger.debug(f"{item['id']} readed")
        with self.lock:
            self.data[found_data[0]] = item

    def run(self):
        RuuviTagSensor.get_datas(self.handle_data)
