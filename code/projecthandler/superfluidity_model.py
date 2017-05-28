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

import copy
import json
import os.path
import yaml
import zipfile
import logging
from lib.util import Util
from StringIO import StringIO

from projecthandler.click_model import ClickProject
from projecthandler.etsi_model import EtsiProject
from lib.superfluidity.superfluidity_parser import SuperfluidityParser
from lib.superfluidity.superfluidity_rdcl_graph import SuperfluidityRdclGraph


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('SuperfluidityModel.py')


PATH_TO_SCHEMAS = 'lib/superfluidity/schemas/'
PATH_TO_DESCRIPTORS_TEMPLATES = 'lib/superfluidity/descriptor_template'
DESCRIPTOR_TEMPLATE_SUFFIX = '.json'
GRAPH_MODEL_FULL_NAME = 'lib/TopologyModels/superfluidity/superfluidity.yaml'
EXAMPLES_FOLDER = 'usecases/SUPERFLUIDITY/'

etsi_elements = ['ns_cp', 'ns_vl', 'vnf', 'vnf_vl', 'vnf_ext_cp', 'vnf_vdu', 'vnf_vdu_cp', 'vnffg']
sf_elements = ['vnf_click_vdu', 'vnf_k8s_vdu']
click_elements = ['element', 'compound_element', 'class_element']


class SuperfluidityProject(EtsiProject, ClickProject):
    """Superfluidity Project class
    The data model has the following descriptors:
        # descrtiptor list in comment #

    """

    @classmethod
    def data_project_from_files(cls, request):

        file_dict = {}
        for my_key in request.FILES.keys():
            file_dict[my_key] = request.FILES.getlist(my_key)

        log.debug(file_dict)

        data_project = SuperfluidityParser.importprojectfiles(file_dict)

        return data_project

    @classmethod
    def data_project_from_example(cls, request):
        superfluidity_id = request.POST.get('example-superfluidity-id', '')
        data_project = SuperfluidityParser.importprojectdir(EXAMPLES_FOLDER + superfluidity_id, 'json')
        return data_project

    @classmethod
    def get_example_list(cls):
        """Returns a list of directories, in each directory there is a project superfluidity"""

        path = EXAMPLES_FOLDER
        dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
        return {'superfluidity': dirs}

    @classmethod
    def get_new_descriptor(cls, descriptor_type, request_id):

        json_template = cls.get_descriptor_template(descriptor_type)

        return json_template

    @classmethod
    def get_descriptor_template(cls, type_descriptor):
        """Returns a descriptor template for a given descriptor type"""

        try:
            schema = Util.loadjsonfile(os.path.join(PATH_TO_DESCRIPTORS_TEMPLATES, type_descriptor + DESCRIPTOR_TEMPLATE_SUFFIX))
            return schema
        except Exception as e:
            log.exception(e)
            return False

    @classmethod
    def get_clone_descriptor(cls, descriptor, type_descriptor, new_descriptor_id):
        new_descriptor = copy.deepcopy(descriptor)

        return new_descriptor

    def get_type(self):
        return "superfluidity"

    def __str__(self):
        return self.name

    def get_overview_data(self):
        current_data = json.loads(self.data_project)
        result = {
            'owner': self.owner.__str__(),
            'name': self.name,
            'updated_date': self.updated_date.__str__(),
            'info': self.info,
            'type': 'superfluidity',
            'nsd': len(current_data['nsd'].keys()) if 'nsd' in current_data else 0,
            'vnfd': len(current_data['vnfd'].keys()) if 'vnfd' in current_data else 0,
            'click': len(current_data['click'].keys()) if 'click' in current_data else 0,
            'k8s': len(current_data['k8s'].keys()) if 'k8s' in current_data else 0,
            'validated': self.validated
        }

        return result

    def get_graph_data_json_topology(self, descriptor_id):
        rdcl_graph = SuperfluidityRdclGraph()
        project = self.get_dataproject()
        topology = rdcl_graph.build_graph_from_project(project,
                                                     model=self.get_graph_model(GRAPH_MODEL_FULL_NAME))
        return json.dumps(topology)

    def create_descriptor(self, descriptor_name, type_descriptor, new_data, data_type):
        """Creates a descriptor of a given type from a json or yaml representation

        Returns the descriptor id or False
        """
        try:
            current_data = json.loads(self.data_project)
            if data_type == 'json':
                new_descriptor = json.loads(new_data)
            elif data_type == 'yaml':
                yaml_object = yaml.load(new_data)
                new_descriptor = json.loads(Util.yaml2json(yaml_object))
            elif data_type == 'click':
                new_descriptor = new_data
            #elif data_type == 'k8s':
            #    new_descriptor = new_data
            else:
                log.debug('Create descriptor: Unknown data type')
                return False


            validate = False
            new_descriptor_id = descriptor_name
            if type_descriptor not in current_data:
                current_data[type_descriptor] = {}
            current_data[type_descriptor][new_descriptor_id] = new_descriptor
            self.data_project = current_data
            self.validated = validate  
            self.update()
            result = new_descriptor_id
        except Exception as e:
            log.exception(e)
            result = False
        return result

    def set_validated(self, value):
        self.validated = True if value is not None and value == True else False

    def get_add_element(self, request):
        result = False
        element_type = request.POST.get('element_type')
        parameters = request.POST.dict()
        print "get_add_element", parameters
        print 'get_add_element', element_type
        if element_type in etsi_elements:
            result = EtsiProject.get_add_element(self, request)
        elif element_type in sf_elements:
            vnf_id = request.POST.get('group_id')
            vdu_id = request.POST.get('element_id')
            if element_type == 'vnf_click_vdu':
                result = self.add_vnf_click_vdu(vnf_id, vdu_id)
            elif element_type == 'vnf_k8s_vdu':
                result = self.add_vnf_k8s_vdu(vnf_id, vdu_id)

        elif element_type in click_elements:
            result = ClickProject.get_add_element(self, request)

        return result

    def get_remove_element(self, request):

        result = False
        parameters = request.POST.dict()
        print "get_remove_element", parameters
        element_type = request.POST.get('element_type')

        if element_type in etsi_elements:
            result = EtsiProject.get_remove_element(self, request)
        elif element_type in sf_elements:
            result = False  #FIXME
        elif element_type in click_elements:
            result = ClickProject.get_remove_element(self, request)

        return result

    def get_add_link(self, request):

        result = False
        parameters = request.POST.dict()
        print "get_add_link", parameters

        source_type = parameters['source_type']
        destination_type = parameters['target_type']

        if source_type in etsi_elements and destination_type in etsi_elements:
            result = EtsiProject.get_add_link(self, request)
        elif source_type in click_elements and destination_type in click_elements:
            result = ClickProject.get_add_link(self, request)
        return result

    def get_remove_link(self, request):

        result = False
        parameters = request.POST.dict()
        print "param remove_link", parameters
        source_type = parameters['source_type']
        destination_type = parameters['target_type']

        if source_type in etsi_elements and destination_type in etsi_elements:
            result = EtsiProject.get_remove_link(self, request)

        return result

    def get_unused_vnf(self, nsd_id):
        try:
            current_data = json.loads(self.data_project)
            result = []
            if 'vnfd' in current_data:
                for vnf in current_data['vnfd']:
                    if vnf not in current_data['nsd'][nsd_id]['vnfdId']:
                        result.append(vnf)
        except Exception as e:
            log.exception(e)
            result = None  # TODO maybe we should use False ?
        return result

    def add_vnf_click_vdu(self, vnf_id, vdu_id):
        log.debug('add_vnf_click_vdu')
        try:
            current_data = json.loads(self.data_project)
            # utility = Util()
            vdu_descriptor = self.get_descriptor_template('vnfd')['vdu'][0]
            vdu_descriptor['vduId'] = vdu_id
            vdu_descriptor['intCpd'] = []
            vdu_descriptor['vduNestedDesc'] = vdu_id
            vdu_descriptor['vduNestedDescType'] = 'click'
            current_data['vnfd'][vnf_id]['vdu'].append(vdu_descriptor)
            if 'click' not in current_data:
                current_data['click'] = {}
            if vdu_id not in current_data['click']:
                current_data['click'][vdu_id] = ''
            self.data_project = current_data
            self.update()
            result = True
        except Exception as e:
            log.exception(e)
            result = False
        return result

    def add_vnf_k8s_vdu(self, vnf_id, vdu_id):
        log.debug('add_vnf_k8s_vdu')
        try:
            current_data = json.loads(self.data_project)
            # utility = Util()
            vdu_descriptor = self.get_descriptor_template('vnfd')['vdu'][0]
            vdu_descriptor['vduId'] = vdu_id
            vdu_descriptor['intCpd'] = []
            vdu_descriptor['vduNestedDesc'] = vdu_id
            vdu_descriptor['vduNestedDescType'] = 'kubernetes'
            current_data['vnfd'][vnf_id]['vdu'].append(vdu_descriptor)
            if 'k8s' not in current_data:
                current_data['k8s'] = {}
            if vdu_id not in current_data['k8s']:
                current_data['k8s'][vdu_id] = ''
            self.data_project = current_data
            self.update()
            result = True
        except Exception as e:
            log.exception(e)
            result = False
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

    def get_deployment_descriptor(self, **kwargs):
        if 'nsdId' in kwargs:
            nsd = kwargs['nsdId']
            rdcl_graph = SuperfluidityRdclGraph()
            return rdcl_graph.build_deployment_descriptor(self.get_dataproject(), nsd)
        else:
            log.debug("no nsdId")
            return {}

    def get_zip_archive(self):
        in_memory = StringIO()
        try:
            current_data = json.loads(self.data_project)
            zip = zipfile.ZipFile(in_memory, "w", zipfile.ZIP_DEFLATED)
            for desc_type in current_data:
                for current_desc in current_data[desc_type]:
                    if desc_type == 'click':
                        zip.writestr(current_desc + '.click', current_data[desc_type][current_desc])
                    elif desc_type == 'k8s':
                        zip.writestr(current_desc + '.yaml',  yaml.dumps(Util.json2yaml(current_data[desc_type][current_desc])))
                    else:
                        zip.writestr(current_desc + '.json', json.dumps(current_data[desc_type][current_desc]))

            zip.close()
        except Exception as e:
            log.debug(e)

        in_memory.flush()
        return in_memory
