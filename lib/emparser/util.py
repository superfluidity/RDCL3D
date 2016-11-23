import json
import yaml
import pyaml
import logging
import jsonschema
import copy

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
            schema = self.loadjsonfile("lib/emparser/schemas/"+type_descriptor+".json")
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
                vnfExtCpd['intVirtualLinkDesc'] = vnfExtCpd['intVirtualLinkDesc'] + new_extention if vnfExtCpd['intVirtualLinkDesc'] is not None else vnfExtCpd['intVirtualLinkDesc']
            for vdu in new_descriptor['vdu']:
                vdu['vduId'] = vdu['vduId'] + new_extention if vdu['vduId'] is not None else vdu['vduId']
                vdu['name'] = vdu['name'] + new_extention if vdu['name'] is not None else vdu['name']
                for intCpd in vdu['intCpd']:
                    intCpd['cpdId'] = intCpd['cpdId'] +  new_extention if intCpd['cpdId'] is not None else intCpd['cpdId']
                    intCpd['intVirtualLinkDesc'] = intCpd['intVirtualLinkDesc'] + new_extention if intCpd['intVirtualLinkDesc'] is not None else intCpd['intVirtualLinkDesc']
            for intVirtualLinkDesc in new_descriptor['intVirtualLinkDesc']:
                intVirtualLinkDesc['virtualLinkDescId'] = intVirtualLinkDesc['virtualLinkDescId'] + new_extention if intVirtualLinkDesc['virtualLinkDescId'] is not None else intVirtualLinkDesc['virtualLinkDescId']
            for deploymentFlavour in new_descriptor['deploymentFlavour']:
                for vduProfile in deploymentFlavour['vduProfile']:
                    vduProfile['vduId'] = vduProfile['vduId'] + new_extention if vduProfile['vduId'] is not None else vduProfile['vduId']
                for virtualLinkProfile in deploymentFlavour['virtualLinkProfile']:
                    virtualLinkProfile['vnfVirtualLinkDescId'] = virtualLinkProfile['vnfVirtualLinkDescId'] + new_extention if virtualLinkProfile['vnfVirtualLinkDescId'] is not None else virtualLinkProfile['vnfVirtualLinkDescId']
        return  new_descriptor
