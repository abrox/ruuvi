import pytest
import json


TEST_JSON =  "{\"values\": [{\"id\": \"C7:41:2E:60:DB:EC\", \"data\": {\"data_format\": 5, \"humidity\": 89.99, \"temperature\": 1.37, \"pressure\": 1012.36, \"acceleration\": 1036.6561628621132, \"acceleration_x\": 8, \"acceleration_y\": 36, \"acceleration_z\": 1036, \"tx_power\": 4, \"battery\": 2767, \"movement_counter\": 192, \"measurement_sequence_number\": 49541, \"mac\": \"c7412e60dbec\"}, \"timestamp\": \"2020-12-04T16:03:05.594277\"}]}"


class TestClass:

    def test_verify_dir_content_ok(self, ):
        json_data = json.loads(TEST_JSON)
        for sensor in json_data['values']:
            print(sensor['data'])
        assert(False)
