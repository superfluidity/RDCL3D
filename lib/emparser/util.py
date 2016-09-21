import json
import yaml
import pyaml
import logging

_lib_name = 'Util'


class Util:

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        self.log = logging.getLogger('UtilLogger')

    def yaml2json(self, object_yaml, name_output):
        self.log.debug('yaml2json')
        return json.dumps(object_yaml, sort_keys=True, indent=2)

    def json2yaml(self, object_json):
        self.log.debug('json2yaml')
        return yaml.safe_dump(object_json, default_flow_style=False)

    def openfile(self, filepath, mode='r', buffering=1):
        self.log.debug('reading file ' + filepath)
        try:
            if isinstance(filepath, file):
                return filepath
            else:
                return open(filepath, mode, buffering)

        except IOError as e:
            self.log.error('IOError: '.format(e.errno, e.strerror))
        raise

    def loadyamlfile(self, name):
        yaml_object = None
        try:
            if isinstance(name, file):
                yaml_object = yaml.load(name)
            else:
                yaml_file = self.openfile(name)
                yaml_object = yaml.load(yaml_file)

            return yaml_object
        except Exception as e:
            self.log.error('Exception loadYamlFile')
            raise

    def loadjsonfile(self, name):
        json_object = None
        try:
            #raise IOError('error from throws')
            if isinstance(name, file):
                json_object = json.load(name)
            else:
                json_file = self.openfile(name)
                json_object = json.load(json_file)

            return json_object
        except Exception as e:
            self.log.error('Exception loadJsonFile')
        raise

    def writejsonfile(self, name, json_object):
        try:
            self.log.debug('writejsonfile ' + name)
            if isinstance(name, file):
                json_object = json.dump(json_object, name)
            else:
                json_file = self.openfile(name, 'w')
                json_object = json.dump(json_object, json_file,separators=(',',': '), indent=4)
        except Exception as e:
            self.log.error('Exception writejsonfile')
            raise

    def writeyamlfile(self, name, yaml_object):
        try:
            self.log.debug('writeyamlfile ' + name)
            if isinstance(name, file):
                yaml_object = pyaml.dump(yaml_object, name, safe=True)
            else:
                yaml_file = self.openfile(name, 'w')
                yaml_object = pyaml.dump(yaml_object, yaml_file, safe=True)
        except Exception as e:
            self.log.error('Exception writeyamlfile')
            raise