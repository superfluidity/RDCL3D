import json
import yaml
import pyaml
import logging
import jsonschema
import copy
import os.path

_lib_name = 'Util'


class Util:

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        self.log = logging.getLogger('UtilLogger')

    def yaml2json(self, object_yaml):
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
            self.log.error('Exception loadJsonFile', e)
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

    def validate_json_schema(self, type_descriptor, data):
        try:
            schema = self.loadjsonfile("lib/etsiparser/schemas/"+type_descriptor+".json")
            jsonschema.validate(data, schema)
            return True
        except Exception as e:
            print e
            self.log.error('Exception validate json schema')
            return False


    def get_descriptor_template(self, type_descriptor):
        try:
            schema = self.loadjsonfile("sf_dev/examples/my_example/"+type_descriptor+"NewComplete.json")
            return schema
        except Exception as e:
            self.log.error('Exception validate json schema')
            return False

    def clone_descriptor (self, descriptor, type_descriptor, new_descriptor_id):
        new_descriptor = copy.deepcopy(descriptor)
        if (type_descriptor == 'vnfd'):
            new_extention = "_"+new_descriptor_id
            new_descriptor['vnfdId'] = new_descriptor_id;
            new_descriptor['vnfProductName'] = new_descriptor['vnfProductName'] + new_extention if new_descriptor['vnfProductName'] is not None else new_descriptor['vnfProductName']
            for vnfExtCpd in new_descriptor['vnfExtCpd']:
                vnfExtCpd['cpdId'] = vnfExtCpd['cpdId'] + new_extention if vnfExtCpd['cpdId'] is not None else vnfExtCpd['cpdId']
        if (type_descriptor == 'nsd'):
            new_extention = "_" + new_descriptor_id
            new_descriptor['nsdIdentifier'] = new_descriptor_id
            new_descriptor['nsdName'] = new_descriptor_id
            new_descriptor['nsdInvariantId'] = new_descriptor_id
            for sapd in new_descriptor['sapd']:
                sapd['cpdId'] = sapd['cpdId'] + new_extention if sapd['cpdId'] is not None else sapd['cpdId']
        return  new_descriptor


    def get_etsi_example_list(self):
        path = 'usecases/ETSI'
        dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
        return dirs

    def get_click_example_list(self):
        path = 'usecases/CLICK'
        dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
        return dirs


    def get_graph_model(self):
        file_path = 'lib/TopologyModels/etsi/etsi.yaml'
        return self.loadyamlfile(file_path)

