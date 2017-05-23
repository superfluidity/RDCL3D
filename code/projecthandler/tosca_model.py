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

from __future__ import unicode_literals

import json
import yaml
import copy
from lib.util import Util
import os.path
import logging

from projecthandler.models import Project
from lib.tosca.tosca_rdcl_graph import ToscaRdclGraph
from lib.tosca.tosca_parser import ToscaParser
from toscaparser.tosca_template import ToscaTemplate
from translator.hot.tosca_translator import TOSCATranslator

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('ToscaModel.py')

PATH_TO_SCHEMAS = 'lib/tosca/schemas/'
PATH_TO_DESCRIPTORS_TEMPLATES = 'lib/tosca/descriptor_template/'
DESCRIPTOR_TEMPLATE_SUFFIX = '.yaml'
GRAPH_MODEL_FULL_NAME = 'lib/TopologyModels/tosca/tosca.yaml'
EXAMPLES_FOLDER = 'usecases/TOSCA/'
PATH_TO_TOSCA_DEFINITION = 'toscaparser/elements/TOSCA_definition_1_0.yaml'


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

        group_id = request.POST.get('group_id')
        element_id = request.POST.get('element_id')
        element_type = request.POST.get('element_type')
        x = request.POST.get('x')
        y = request.POST.get('y')
        current_data = json.loads(self.data_project)
        tosca_definition = Util().loadyamlfile(PATH_TO_TOSCA_DEFINITION)
        node_types = {}
        node_types.update(tosca_definition['node_types'])
        new_element = {}
        new_element['type'] = element_type
        type_definition =  node_types[element_type]
        while element_type in node_types:
            type_definition = node_types[element_type]
            if 'properties' in type_definition:
                for propriety in type_definition['properties']:
                    if 'required' not in type_definition['properties'][propriety] or type_definition['properties'][propriety]['required']:
                        if 'properties' not in new_element:
                            new_element['properties'] = {}
                        if propriety == 'version':
                            new_element['properties'][propriety] = 1.0
                        else:
                            if type_definition['properties'][propriety]['type'] == 'scalar-unit.size':
                                new_element['properties'][propriety] = '1 MB'
                            else:
                               new_element['properties'][propriety] = 'prova'
            element_type = type_definition['derived_from'] if 'derived_from' in type_definition else None
        if 'node_templates' not in current_data['toscayaml'][group_id]['topology_template'] or current_data['toscayaml'][group_id]['topology_template']['node_templates'] is None:
            current_data['toscayaml'][group_id]['topology_template']['node_templates'] = {}
        current_data['toscayaml'][group_id]['topology_template']['node_templates'][element_id] = new_element
        if 'positions' not in current_data:
            current_data['positions'] = {}
        if 'vertices' not in current_data['positions']:
            current_data['positions']['vertices'] = {}
        if element_id not in current_data['positions']['vertices']:
            current_data['positions']['vertices'][element_id] = {}
        current_data['positions']['vertices'][element_id]['x'] = x
        current_data['positions']['vertices'][element_id]['y'] = y
        self.data_project = current_data
        # self.validated = validate #TODO(stefano) not clear if this is the validation for the whole project
        self.update()
        result = True
        return result        

    def get_remove_element(self, request):
        group_id = request.POST.get('group_id')
        element_id = request.POST.get('element_id')
        element_type = request.POST.get('element_type')
        parameters = request.POST.dict()
        print "get_remove_element", parameters
        current_data = json.loads(self.data_project)
        if element_id in current_data['toscayaml'][group_id]['topology_template']['node_templates']: del current_data['toscayaml'][group_id]['topology_template']['node_templates'][element_id]
        for key in current_data['toscayaml'][group_id]['topology_template']['node_templates']:
            node = current_data['toscayaml'][group_id]['topology_template']['node_templates'][key]
            if 'requirements' in node:
                for r in node ['requirements']:
                    for key in r.keys():
                        if r[key] == element_id:
                            node['requirements'].remove(r)
        self.data_project = current_data
        # self.validated = validate #TODO(stefano) not clear if this is the validation for the whole project
        self.update()
        result = True

        return result        

    def get_add_link(self, request):
        result = False
        parameters = request.POST.dict()
        link = json.loads(parameters['link'])
        source = link['source']
        destination = link['target']
        source_type = source['info']['type']
        destination_type = destination['info']['type']
        source_id = source['id']
        destination_id = destination['id']
        group = source['info']['group'][0]
        current_data = json.loads(self.data_project)
        tosca_definition = Util().loadyamlfile(PATH_TO_TOSCA_DEFINITION)
        added = False
        if 'requirements' in tosca_definition['node_types'][source_type]:
            for req in tosca_definition['node_types'][source_type]['requirements']:
                for key in req:
                    if req[key]['node'] == destination_type:
                        added = True
                        if 'requirements' not in current_data['toscayaml'][group]['topology_template']['node_templates'][
                            source_id] or \
                                        current_data['toscayaml'][group]['topology_template']['node_templates'][source_id][
                                            'requirements'] is None:
                            current_data['toscayaml'][group]['topology_template']['node_templates'][source_id][
                                'requirements'] = []
                        requirements = current_data['toscayaml'][group]['topology_template']['node_templates'][source_id][
                            'requirements']
                        element = next((x for x in requirements if key in x.keys()), None)
                        if element is not None:
                            element[key] = destination_id
                        else:
                            element = {}
                            element[key] = destination_id
                            requirements.append(element)
        if not added and 'requirements' in tosca_definition['node_types'][destination_type]:
            for req in tosca_definition['node_types'][destination_type]['requirements']:
                for key in req:
                    if req[key]['node'] == source_type:
                        added = True
                        if 'requirements' not in \
                                current_data['toscayaml'][group]['topology_template']['node_templates'][
                                    destination_id] or \
                                        current_data['toscayaml'][group]['topology_template']['node_templates'][
                                            destination_id][
                                            'requirements'] is None:
                            current_data['toscayaml'][group]['topology_template']['node_templates'][destination_id][
                                'requirements'] = []
                        requirements = \
                        current_data['toscayaml'][group]['topology_template']['node_templates'][destination_id][
                            'requirements']
                        element = next((x for x in requirements if key in x.keys()), None)
                        if element is not None:
                            element[key] = source_id
                        else:
                            element = {}
                            element[key] = source_id
                            requirements.append(element)

        self.data_project = current_data
        # self.validated = validate #TODO(stefano) not clear if this is the validation for the whole project
        self.update()
        result = True
        return result

    def get_remove_link(self, request):
        result = False
        parameters = request.POST.dict()
        link = json.loads(parameters['link'])
        source = link['source']
        destination = link['target']
        source_type = source['info']['type']
        destination_type = destination['info']['type']
        source_id = source['id']
        destination_id = destination['id']
        group = source['info']['group'][0]
        current_data = json.loads(self.data_project)
        tosca_definition = Util().loadyamlfile(PATH_TO_TOSCA_DEFINITION)
        removed = False
        if 'requirements' in tosca_definition['node_types'][source_type]:
            for req in tosca_definition['node_types'][source_type]['requirements']:
                for key in req:
                    if req[key]['node'] == destination_type:
                        if 'requirements' not in \
                                current_data['toscayaml'][group]['topology_template']['node_templates'][
                                    source_id] or \
                                        current_data['toscayaml'][group]['topology_template']['node_templates'][
                                            source_id][
                                            'requirements'] is None:
                            current_data['toscayaml'][group]['topology_template']['node_templates'][source_id][
                                'requirements'] = []
                        requirements = \
                        current_data['toscayaml'][group]['topology_template']['node_templates'][source_id][
                            'requirements']
                        element = next((x for x in requirements if key in x.keys()), None)
                        if element is not None:
                            removed = True
                            requirements = \
                            current_data['toscayaml'][group]['topology_template']['node_templates'][source_id][
                                'requirements'].remove(element)
        if not removed and 'requirements' in tosca_definition['node_types'][destination_type]:
            for req in tosca_definition['node_types'][destination_type]['requirements']:
                for key in req:
                    if req[key]['node'] == source_type:
                        if 'requirements' not in \
                                current_data['toscayaml'][group]['topology_template']['node_templates'][
                                    destination_id] or \
                                        current_data['toscayaml'][group]['topology_template']['node_templates'][
                                            destination_id][
                                            'requirements'] is None:
                            current_data['toscayaml'][group]['topology_template']['node_templates'][destination_id][
                                'requirements'] = []
                        requirements = \
                            current_data['toscayaml'][group]['topology_template']['node_templates'][destination_id][
                                'requirements']
                        element = next((x for x in requirements if key in x.keys()), None)
                        if element is not None:
                            removed = True
                            requirements = \
                            current_data['toscayaml'][group]['topology_template']['node_templates'][destination_id][
                                'requirements'].remove(element)

        self.data_project = current_data
        # self.validated = validate #TODO(stefano) not clear if this is the validation for the whole project
        self.update()
        result = True
        result = True


        return result

    def get_available_nodes(self, args):
        """Returns all available node """
        log.debug('get_available_nodes')
        try:
            result = []
            #current_data = json.loads(self.data_project)
            model_graph = self.get_graph_model(GRAPH_MODEL_FULL_NAME)
            for node in model_graph['layer'][args['layer']]['nodes']:
                if 'addable' in model_graph['layer'][args['layer']]['nodes'][node] and model_graph['layer'][args['layer']]['nodes'][node]['addable']:
                    current_data = {
                        "id": node,
                        "category_name": model_graph['nodes'][node]['label'],
                        "types": [
                            {
                                "name": "generic",
                                "id": node
                            }
                        ]
                    }
                    result.append(current_data)

            #result = current_data[type_descriptor][descriptor_id]
        except Exception as e:
            log.debug(e)
            result = []
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


