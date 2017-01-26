from __future__ import unicode_literals

import json
import yaml
import copy
from lib.util import Util
import os.path
from projecthandler.models import Project

from lib.tosca.tosca_rdcl_graph import ToscaRdclGraph
from lib.tosca.tosca_parser import ToscaParser
from toscaparser.tosca_template import ToscaTemplate
from translator.hot.tosca_translator import TOSCATranslator


PATH_TO_SCHEMAS = 'lib/tosca/schemas/'
PATH_TO_DESCRIPTORS_TEMPLATES = 'sf_dev/examples/my_example/'
DESCRIPTOR_TEMPLATE_SUFFIX = 'NewComplete.json'
GRAPH_MODEL_FULL_NAME = 'lib/TopologyModels/tosca/tosca.yaml'
EXAMPLES_FOLDER = 'usecases/TOSCA/'

class ToscaProject(Project):
    """Tosca class

    The data model has the following descriptors:
    'toscayaml'

    """


    @classmethod
    def data_project_from_files(cls, request):

        file_dict = {}
        for my_key in request.FILES.keys():
            file_dict [my_key]= request.FILES.getlist(my_key)

        data_project = ToscaParser.importprojectfiles(file_dict)
        print "data project read from files:"
        print data_project
        return data_project

    @classmethod
    def data_project_from_example(cls, request):
        example_id = request.POST.get('example-tosca-id', '')
        data_project = ToscaParser.importprojectdir(EXAMPLES_FOLDER + example_id + '/YAML', 'yaml')
        print "data project read from directory:"
        print data_project
        # data_project = importprojectdir('usecases/TOSCA/' + example_id + '/JSON', 'json')
        return data_project

    @classmethod
    def get_example_list(cls):
        """Returns a list of directories, in each directory there is a project example"""

        path = EXAMPLES_FOLDER
        dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
        return {'tosca' : dirs}

    # @classmethod
    # def get_graph_model(cls):
    #     """Returns the model of the graph of the project type as a yaml object

    #     Returns an empty dict if there is no file with the model
    #     """
    #     file_path = GRAPH_MODEL_FULL_NAME
    #     graph_model = {}
    #     try:
    #         graph_model = Util.loadyamlfile(file_path)
    #     except Exception as e:
    #         pass
    #     return graph_model       

    @classmethod
    def get_json_schema_by_type(cls, type_descriptor):
        schema = PATH_TO_SCHEMAS+type_descriptor+".json"
        return schema        

    @classmethod
    def get_new_descriptor(cls,descriptor_type, request_id):
        # util = Util()

        json_template = cls.get_descriptor_template(descriptor_type)
        if descriptor_type == 'toscayaml':
            pass
            # json_template['nsdIdentifier'] = request_id
            # json_template['nsdInvariantId'] = request_id
        else:
            return {}

        return json_template

    @classmethod
    def get_descriptor_template(cls, type_descriptor):
        """Returns a descriptor template for a given descriptor type"""
        
        try:
            #schema = Util.loadjsonfile(PATH_TO_DESCRIPTORS_TEMPLATES+type_descriptor+DESCRIPTOR_TEMPLATE_SUFFIX)
            # print 'type_descriptor : '+type_descriptor
            #FixMe bisogna creare un template
            yaml_object = Util().loadyamlfile('usecases/TOSCA/One-Server-Three-Networks/YAML/tosca_one_server_three_networks.yaml')
            toscajson = json.loads(Util.yaml2json(yaml_object))
            return toscajson
        except Exception as e:
            # log.error('Exception in get descriptor template') #TODO(stefano) add logging
            print 'Exception in get descriptor template'
            return False

    @classmethod
    def get_clone_descriptor (cls, descriptor, type_descriptor, new_descriptor_id):
        new_descriptor = copy.deepcopy(descriptor)

        return  new_descriptor



    def get_type(self):
        return "tosca"

    def __str__(self):
        return self.name

    def get_overview_data(self):
        current_data = json.loads(self.data_project)
        result = {
            'owner': self.owner.__str__(),
            'name': self.name,
            'updated_date': self.updated_date.__str__(),
            'info': self.info,
            'type': 'tosca',
            'toscayaml' : len(current_data['toscayaml'].keys()) if 'toscayaml' in current_data else 0,
            # 'nsd': len(current_data['nsd'].keys()) if 'nsd' in current_data else 0,
            # 'vnffgd': len(current_data['vnffgd'].keys()) if 'vnffgd' in current_data else 0,
            # 'vld': len(current_data['vld'].keys()) if 'vld' in current_data else 0,
            # 'vnfd': len(current_data['vnfd'].keys()) if 'vnfd' in current_data else 0,
            'validated': self.validated
        }

        return result

    def get_graph_data_json_topology(self, descriptor_id):
        test_t3d = ToscaRdclGraph()
        project = self.get_dataproject()
        topology = test_t3d.build_graph_from_project(project,
                                    model=self.get_graph_model(GRAPH_MODEL_FULL_NAME))

        # print json.dumps(topology)

        return json.dumps(topology)

    def create_descriptor(self, descriptor_name, type_descriptor, new_data, data_type):
        """Creates a descriptor of a given type from a json or yaml representation

        Returns the descriptor id or False
        """
        result = False
        try:
            print type_descriptor, data_type
            current_data = json.loads(self.data_project)
            if data_type == 'json':
                new_descriptor = json.loads(new_data)
            elif data_type == 'yaml':
                # utility = Util()
                yaml_object = yaml.load(new_data)
                new_descriptor = json.loads(Util.yaml2json(yaml_object))
            else:
                print 'Unknown data type'
                return False

            if type_descriptor == 'toscayaml':

                if descriptor_name is None: 
                    new_descriptor_id = Util.get_unique_id()
                else:
                    new_descriptor_id = descriptor_name 
                if not type_descriptor in current_data:
                    current_data[type_descriptor] = {}
                current_data[type_descriptor][new_descriptor_id] = new_descriptor
                self.data_project = current_data
                #self.validated = validate #TODO(stefano) not clear if this is the validation for the whole project
                self.update()
                result = new_descriptor_id

            else:
                return False

        except Exception as e:
            print 'Exception in create descriptor', e
        return result


    def set_validated(self, value):
        self.validated = True if value is not None and value == True else False


    def get_add_element(self, request):

        result = False

        return result        

    def get_remove_element(self, request):

        result = False

        return result        

    def get_add_link(self, request):

        result = False

        return result        

    def get_remove_link(self, request):

        result = False

        return result        

    def get_generatehotemplate(self, request, descriptor_id, descriptor_type):
        """ Generate hot template for a TOSCA descriptor

        It is based on the reverse engineering of translator/shell.py 
        """

        result = ''
        print "get_generatehotemplate"
        print "descriptor_id: "+ descriptor_id
        print "descriptor_type: "+ descriptor_type


        project = self.get_dataproject()

        print project['toscayaml'][descriptor_id]

        tosca = ToscaTemplate(None, {}, False, yaml_dict_tpl=project['toscayaml'][descriptor_id])
        translator = TOSCATranslator(tosca, {}, False, csar_dir=None)

        #log.debug(_('Translating the tosca template.'))
        print 'Translating the tosca template.'
        print translator.translate()
        result = translator.translate()

        return result


