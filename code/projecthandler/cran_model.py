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
from lib.util import Util
import logging
from projecthandler.models import Project

from lib.cran.cran_parser import CranParser
from lib.cran.cran_rdcl_graph import CranRdclGraph


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('CranModel.py')


PATH_TO_SCHEMAS = 'lib/cran/schemas/'
PATH_TO_DESCRIPTORS_TEMPLATES = 'lib/cran/descriptor_template'
DESCRIPTOR_TEMPLATE_SUFFIX = '.yaml'
GRAPH_MODEL_FULL_NAME = 'lib/TopologyModels/cran/cran.yaml'
EXAMPLES_FOLDER = 'usecases/CRAN/'


class CranProject(Project):
    """Cran Project class
    The data model has the following descriptors:
        # descrtiptor list in comment #

    """

    @classmethod
    def data_project_from_files(cls, request):

        file_dict = {}
        for my_key in request.FILES.keys():
            file_dict[my_key] = request.FILES.getlist(my_key)

        log.debug(file_dict)

        data_project = CranParser.importprojectfiles(file_dict)

        return data_project

    @classmethod
    def data_project_from_example(cls, request):
        cran_id = request.POST.get('example-cran-id', '')
        data_project = CranParser.importprojectdir(EXAMPLES_FOLDER + cran_id , 'yaml')
        return data_project

    @classmethod
    def get_example_list(cls):
        """Returns a list of directories, in each directory there is a project cran"""

        path = EXAMPLES_FOLDER
        dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
        return {'cran': dirs}

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
        return "cran"

    def __str__(self):
        return self.name

    def get_overview_data(self):
        current_data = json.loads(self.data_project)
        result = {
            'owner': self.owner.__str__(),
            'name': self.name,
            'updated_date': self.updated_date.__str__(),
            'info': self.info,
            'type': 'cran',
            'cran': len(current_data['cran'].keys()) if 'cran' in current_data else 0,

            'validated': self.validated
        }

        return result

    def get_graph_data_json_topology(self, descriptor_id):
        rdcl_graph = CranRdclGraph()
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
            else:
                log.debug('Create descriptor: Unknown data type')
                return False

            # schema = cls.loadjsonfile("lib/cran/schemas/"+type_descriptor+".json")
            #reference_schema = self.get_json_schema_by_type(type_descriptor)
            # validate = Util.validate_json_schema(reference_schema, new_descriptor)
            validate = False
            new_descriptor_id = descriptor_name
            if not type_descriptor in current_data:
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


    def get_available_nodes(self, args):
        """Returns all available node """
        log.debug('get_available_nodes')
        try:
            result = []
            #current_data = json.loads(self.data_project)
            model_graph = self.get_graph_model(GRAPH_MODEL_FULL_NAME)
            for node in model_graph['layer'][args['layer']]['nodes']:

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