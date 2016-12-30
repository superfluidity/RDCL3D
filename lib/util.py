import json
import yaml
import pyaml
import logging
import jsonschema
# import copy
import os.path

_lib_name = 'Util'


logging.basicConfig(level=logging.DEBUG)
fh = logging.FileHandler('rdcl.log')
log = logging.getLogger('UtilLogger')
log.addHandler(fh)

class Util(object):

    def __init__(self):
        # logging.basicConfig(level=logging.DEBUG)
        # self.log = logging.getLogger('UtilLogger')
        pass

    @classmethod
    def yaml2json(cls, object_yaml):
        """Converts a yaml object into a json representation"""

        log.debug('yaml2json')
        return json.dumps(object_yaml, sort_keys=True, indent=2)

    @classmethod
    def json2yaml(cls, object_json):
        log.debug('json2yaml')
        return yaml.safe_dump(object_json, default_flow_style=False)

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
            log.error('IOError: '.format(e.errno, e.strerror))
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
            log.error('Exception loadYamlFile')
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
            log.error('Exception loadJsonFile', e)
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
            log.error('Exception writejsonfile')
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
            log.error('Exception writeyamlfile')
            raise

    @classmethod
    def validate_json_schema(cls, reference_schema, data):
        """Validates a json data against a json schema

        Raises Exception
        """

        try:
            # schema = cls.loadjsonfile("lib/etsi/schemas/"+type_descriptor+".json")
            # print 'type_descriptor : '+type_descriptor
            jsonschema.validate(data, reference_schema)
            return True
        except Exception as e:
            print e
            log.error('Exception validate json schema')
            return False

    # @classmethod
    # def get_descriptor_template(cls, type_descriptor):
    #     """Returns a descriptor template for a given descriptor type"""

    #     try:
    #         schema = cls.loadjsonfile("sf_dev/examples/my_example/"+type_descriptor+"NewComplete.json")
    #         # print 'type_descriptor : '+type_descriptor
    #         return schema
    #     except Exception as e:
    #         log.error('Exception in get descriptor template')
    #         return False

    # @classmethod
    # def get_clone_descriptor (cls, descriptor, type_descriptor, new_descriptor_id):
    #     new_descriptor = copy.deepcopy(descriptor)
    #     if (type_descriptor == 'vnfd'):
    #         new_extention = "_"+new_descriptor_id
    #         new_descriptor['vnfdId'] = new_descriptor_id;
    #         new_descriptor['vnfProductName'] = new_descriptor['vnfProductName'] + new_extention if new_descriptor['vnfProductName'] is not None else new_descriptor['vnfProductName']
    #         for vnfExtCpd in new_descriptor['vnfExtCpd']:
    #             vnfExtCpd['cpdId'] = vnfExtCpd['cpdId'] + new_extention if vnfExtCpd['cpdId'] is not None else vnfExtCpd['cpdId']
    #     if (type_descriptor == 'nsd'):
    #         new_extention = "_" + new_descriptor_id
    #         new_descriptor['nsdIdentifier'] = new_descriptor_id
    #         new_descriptor['nsdName'] = new_descriptor_id
    #         new_descriptor['nsdInvariantId'] = new_descriptor_id
    #         for sapd in new_descriptor['sapd']:
    #             sapd['cpdId'] = sapd['cpdId'] + new_extention if sapd['cpdId'] is not None else sapd['cpdId']
    #     return  new_descriptor


    # def get_etsi_example_list(self):
    #     path = 'usecases/ETSI'
    #     dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    #     return dirs

    # def get_click_example_list(self):
    #     path = 'usecases/CLICK'
    #     dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    #     return dirs


    # def get_graph_model(self):
    #     file_path = 'lib/TopologyModels/etsi/etsi.yaml'
    #     return self.loadyamlfile(file_path)
