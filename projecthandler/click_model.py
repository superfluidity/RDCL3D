from __future__ import unicode_literals

import json
from lib.util import Util
from projecthandler.models import Project
from lib.clickparser import click_parser
import os.path
import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('ClickModel.py')

EXAMPLES_FOLDER = 'usecases/CLICK/'
GRAPH_MODEL_FULL_NAME = 'lib/TopologyModels/click/click.yaml'

class ClickProject(Project):
    @classmethod
    def data_project_from_files(cls, request):

        cfg_files = request.FILES.getlist('cfg_files')
        data_project = click_parser.importprojectfile(cfg_files)
        return data_project

    @classmethod
    def data_project_from_example(cls, request):
        ##FIXME
        example_id = request.POST.get('example-click-id', '')
        data_project = click_parser.importprojectdir(EXAMPLES_FOLDER + example_id , 'click')
        return data_project

    @classmethod
    def get_example_list(cls):
        dirs = [d for d in os.listdir(EXAMPLES_FOLDER) if os.path.isdir(os.path.join(EXAMPLES_FOLDER, d))]
        return {'click': dirs}

    @classmethod
    def get_new_descriptor(cls, descriptor_type, request_id):

        json_template = ''
        return json_template

    def get_type(self):
        return "click"

    def __str__(self):
        return self.name

    def get_overview_data(self):
        current_data = json.loads(self.data_project)
        result = {
            'owner': self.owner.__str__(),
            'name': self.name,
            'updated_date': self.updated_date.__str__(),
            'info': self.info,
            'type': 'click',
            'click': len(current_data['click'].keys()) if 'click' in current_data else 0,
            'validated': self.validated
        }

        return result

    def get_graph_data_json_topology(self, descriptor_id):
        current_data = json.loads(self.data_project)
        topology = click_parser.importprojectjson(current_data, model=self.get_graph_model(GRAPH_MODEL_FULL_NAME), positions= self.get_positions() )
        return json.dumps(topology)

    def create_descriptor(self, descriptor_name, type_descriptor, new_data, data_type):
        try:
            print type_descriptor, data_type, descriptor_name
            current_data = json.loads(self.data_project)
            if data_type == 'click':
                new_descriptor = new_data

            if not type_descriptor in current_data:
                current_data[type_descriptor] = {}
            current_data[type_descriptor][descriptor_name] = new_descriptor
            self.data_project = current_data
            self.validated = False
            self.update()
            result = descriptor_name  ##FIXME
        except Exception as e:
            log.exception(e)
            result = False
        return result


