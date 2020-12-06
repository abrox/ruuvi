import pytest
import json
from collector import Collector

ID = 'C7:41:2E:60:DB:EC'
NOT_ID = 'C7:41:2E:60:DB:CC'
TEST_DATA =  {'id': 'C7:41:2E:60:DB:EC', 'data': {'data_format': 5, 'humidity': 89.99, 'temperature': 1.37, 'pressure': 1012.36, 'acceleration': 1036.6561628621132, 'acceleration_x': 8, 'acceleration_y': 36, 'acceleration_z': 1036, 'tx_power': 4, 'battery': 2767, 'movement_counter': 192, 'measurement_sequence_number': 49541, 'mac': 'c7412e60dbec'}, 'timestamp': '2020-12-04T16:03:05.594277'}


class TestClass:
    @pytest.fixture(scope="class")
    def ruuvi(self, tmpdir_factory):
        Collector.CreateCollector()
        c = Collector.getClient()
        c.data = { ID: TEST_DATA}
        return c
        

    def test_get_sensor_latest_ok(self, ruuvi):
        data = ruuvi.get_sensor_latest(ID)
        assert(data['id'] == ID)

    def test_get_sensor_latest_not_ok(self, ruuvi):
        with pytest.raises(KeyError):
            ruuvi.get_sensor_latest(NOT_ID)
        
