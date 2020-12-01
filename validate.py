#!/usr/bin/env python3
import jsonschema
from jsonschema import validate
from os.path import join, dirname, abspath
import jsonref


def _load_json_schema(filename):
    """ Loads the given schema file """

    # relative_path = join('', filename)
    relative_path = filename
    absolute_path = join(dirname(__file__), relative_path)
    absolute_path = abspath(relative_path)
    base_path = dirname(absolute_path)
    base_uri = 'file://{}/'.format(base_path)

    with open(absolute_path) as schema_file:
        return jsonref.loads(schema_file.read(),
                             base_uri=base_uri,
                             jsonschema=True)


def validate_json(json_data, schema):
    """REF: https://json-schema.org/ """
    # Describe what kind of json you expect.
    execute_api_schema = _load_json_schema(schema)

    try:
        validate(instance=json_data, schema=execute_api_schema)
    except jsonschema.exceptions.ValidationError as err:
        print(err)
        err = "Given JSON data is InValid"
        return False, err

    message = "Given JSON data is Valid"
    return True, message
