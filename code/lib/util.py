#
#   Copyright 2017 CNIT - Consorzio Nazionale Interuniversitario per le Telecomunicazioni
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an  BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

import json
import yaml
import pyaml
import logging
import jsonschema
import uuid 

_lib_name = 'Util'


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('lib/util.py')


class Util(object):

    def __init__(self):
        # logging.basicConfig(level=logging.DEBUG)
        # self.log = logging.getLogger('UtilLogger')
        pass


    @classmethod
    def json_load_byteified(cls, file_handle):
        return cls._byteify(
            json.load(file_handle, object_hook=cls._byteify),
            ignore_dicts=True
        )

    @classmethod
    def json_loads_byteified(cls, json_text):
        return cls._byteify(
            json.loads(json_text, object_hook=cls._byteify),
            ignore_dicts=True
        )

    @classmethod
    def _byteify(cls, data, ignore_dicts = False):
        # if this is a unicode string, return its string representation
        if isinstance(data, unicode):
            return data.encode('utf-8')
        # if this is a list of values, return list of byteified values
        if isinstance(data, list):
            return [ cls._byteify(item, ignore_dicts=True) for item in data ]
        # if this is a dictionary, return dictionary of byteified keys and values
        # but only if we haven't already byteified it
        if isinstance(data, dict) and not ignore_dicts:
            return {
                cls._byteify(key, ignore_dicts=True): cls._byteify(value, ignore_dicts=True)
                for key, value in data.iteritems()
            }
        # if it's anything else, return it in its original form
        return data

    @classmethod
    def yaml2json(cls, object_yaml):
        """Converts a yaml object into a json representation"""
        log.debug('yaml2json')
        return json.dumps(object_yaml, sort_keys=True, indent=2) if not object_yaml is None else None

    @classmethod
    def json2yaml(cls, object_json):
        """Converts a json object into a yaml representation"""
        log.debug('json2yaml')
        return yaml.safe_dump(object_json, default_flow_style=False) if not object_json is None else None

    @classmethod
    def openfile(cls, filepath, mode='r', buffering=1):
        """Returns an open file given a filepath

        If the filepath is already an open file, returns into
        Raises Exception
        """

        log.debug('reading file ' + filepath)
        try:
            if isinstance(filepath, file):
                return filepath
            else:
                return open(filepath, mode, buffering)

        except IOError as e:
            log.exception('openfile', e)
            raise

    @classmethod
    def loadyamlfile(cls, name):
        """Returns a yaml object from a filename or an open file

        Raises Exception
        """

        yaml_object = None
        try:
            if isinstance(name, file):
                yaml_object = yaml.load(name)
            else:
                yaml_file = cls.openfile(name)
                yaml_object = yaml.load(yaml_file)

            return yaml_object
        except Exception as e:
            log.exception('Exception loadYamlFile', e)
            raise

    @classmethod
    def loadjsonfile(cls, name):
        """Returns a json object from a filename or an open file

        Raises Exception
        """

        json_object = None
        try:
            #raise IOError('error from throws')
            if isinstance(name, file):
                json_object = json.load(name)
            else:
                # json_file = self.openfile(name)
                json_file = cls.openfile(name)
                json_object = json.load(json_file)

            return json_object
        except Exception as e:
            log.exception('Exception loadJsonFile', e)
            raise

    @classmethod
    def writejsonfile(cls, name, json_object):
        """Writes the dump of a json obj to a filename or an open file

        Raises Exception
        """

        try:
            log.debug('writejsonfile ' + name)
            if isinstance(name, file):
                json_object = json.dump(json_object, name)
            else:
                json_file = cls.openfile(name, 'w')
                json_object = json.dump(json_object, json_file,separators=(',',': '), indent=4)
        except Exception as e:
            log.exception('Exception writejsonfile', e)
            raise

    @classmethod
    def writeyamlfile(cls, name, yaml_object):
        """Writes the dump of a yaml obj to a filename or an open file

        Raises Exception
        """

        try:
            log.debug('writeyamlfile ' + name)
            if isinstance(name, file):
                yaml_object = pyaml.dump(yaml_object, name, safe=True)
            else:
                yaml_file = cls.openfile(name, 'w')
                yaml_object = pyaml.dump(yaml_object, yaml_file, safe=True)
        except Exception as e:
            log.exception('Exception writeyamlfile')
            raise

    @classmethod
    def validate_json_schema(cls, reference_schema, data):
        """Validates a json data against a json schema

        Raises Exception
        """

        try:
            # schema = cls.loadjsonfile("lib/etsi/schemas/"+type_descriptor+".json")
             #print 'type_descriptor : '+type_descriptor
            jsonschema.validate(data, reference_schema)
            return True
        except Exception as e:
            log.exception('Exception validate json schema', e)
            return False

    @classmethod
    def get_unique_id(cls):
        return uuid.uuid4().hex[:6].upper()
