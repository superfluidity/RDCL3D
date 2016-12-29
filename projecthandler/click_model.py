from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
import jsonfield
from StringIO import StringIO
import zipfile
import json
import yaml
from lib.util import Util
# from model_utils.managers import InheritanceManager
from projecthandler.models import Project
from lib.clickparser import mainrdcl
import os.path


class ClickProject(Project):

    @classmethod
    def data_project_from_files(cls, request):

        cfg_files = request.FILES.getlist('cfg_files')
        data_project = mainrdcl.importprojectfile(cfg_files)
        return data_project

    @classmethod
    def data_project_from_example(cls, request):
        ##FIXME
        example_id = request.POST.get('example-click-id', '')
        data_project = {}
        return data_project
    
    @classmethod
    def get_example_list(cls):
        path = 'usecases/CLICK'
        dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
        return dirs        

    @classmethod
    def get_new_descriptor(cls,descriptor_type, request_id):

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
        project = self.get_descriptor(descriptor_id, self.get_type())
        topology = mainrdcl.importprojectjson(project)
        return topology


    # def get_descriptors(self, type_descriptor):
    #     try:
    #         current_data = json.loads(self.data_project)
    #         result = current_data[type_descriptor]
    #         print result
    #     except Exception:
    #         result = {}
    #     return result

    # def get_descriptor(self, descriptor_id, type_descriptor):
    #     try:
    #         current_data = json.loads(self.data_project)
    #         result = current_data[type_descriptor][descriptor_id]
    #     except Exception:
    #         result = {}

    #     return result

    # def delete_descriptor(self, type_descriptor, descriptor_id):
    #     try:
    #         print descriptor_id, type_descriptor
    #         current_data = json.loads(self.data_project)
    #         del (current_data[type_descriptor][descriptor_id])
    #         self.data_project = current_data
    #         self.update()
    #         result = True
    #     except Exception as e:
    #         print 'exception', e
    #         result = False
    #     return result

    def create_descriptor(self, descriptor_name, type_descriptor, new_data, data_type):
        try:
            utility = Util()
            print type_descriptor, data_type
            current_data = json.loads(self.data_project)
            if data_type == 'json':
                new_descriptor = json.loads(new_data)

            if not type_descriptor in current_data:
                current_data[type_descriptor] = {}
            current_data[type_descriptor][descriptor_name] = new_descriptor
            self.data_project = current_data
            self.validated = False
            self.update()
            result = descriptor_name  ##FIXME
        except Exception as e:
            print 'exception create descriptor', e
            result = False
        return result

    # def set_data_project(self, new_data, validated):
    #     self.data_project = new_data
    #     self.set_validated(validated)
    #     self.update()

    # def edit_graph_positions(self, positions):
    #     print positions
    #     try:
    #         current_data = json.loads(self.data_project)
    #         if 'positions' not in current_data:
    #             current_data['positions'] = {}
    #         if 'vertices' not in current_data['positions']:
    #             current_data['positions']['vertices'] = {}
    #         if 'vertices' in positions:
    #             current_data['positions']['vertices'].update(positions['vertices'])
    #         self.data_project = current_data
    #         self.update()
    #         result = True
    #     except Exception as e:
    #         print 'exception', e
    #         result = False
    #     return result


# Project.add_project_type('click', ClickProject)