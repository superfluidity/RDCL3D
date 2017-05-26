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
import os.path
import logging
import re

from projecthandler.models import Project
from lib.clickparser import click_parser

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
        topology = click_parser.importprojectjson(current_data, model=self.get_graph_model(GRAPH_MODEL_FULL_NAME), positions=self.get_positions() )
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

    # TODO modificare l'add_element credo non sia corretto
    def get_add_element(self, request):
        print "click add element"
        result = False
        current_data = json.loads(self.data_project)
        group_id = request.POST.get('group_id')
        element_id = request.POST.get('element_id')
        element_type = request.POST.get('element_type')
        desc_id = request.POST.get('element_desc_id')
        print "click add", group_id, element_id, element_type, desc_id
        if element_type == 'class_element':
            class_id = element_id.title()
            lines = current_data['click'][desc_id].splitlines(True)
            for line in lines:
                if '//' not in line:
                    lines = lines[:lines.index(line)] + ["elementclass "+class_id+" {\n};\n"] + lines[lines.index(line):]
                    current_data['click'][desc_id] = ''.join(lines)
                    break
        else:
            class_id = "PullTee"
        if group_id != desc_id:
            group_id = group_id[group_id.rfind(".")+1:]
            print group_id, desc_id
            lines = current_data['click'][desc_id].splitlines(True)
            for line in lines:
                if group_id+" ::" in line:
                    end = line.rfind("(")  if line.rfind("(") != -1 else line.rfind(";")
                    element_class = line[line.rfind("::") + 2:end]
            for line in lines:
                check = element_class+" {"
                print check
                if check in line:
                    lines = lines[:lines.index(line)+1] + [ element_id + " :: "+class_id+" ;\n"] + lines[lines.index(line)+1:]
                    current_data['click'][desc_id] = ''.join(lines)
                    break

        else:
            current_data['click'][desc_id] +=  element_id + " :: "+class_id+" ;\n"
        self.data_project = current_data
        self.update()
        result = True
        return result

    def get_remove_element(self, request):

        result = False
        current_data = json.loads(self.data_project)
        group_id = request.POST.get('group_id')
        element_id = request.POST.get('element_id')
        element_type = request.POST.get('element_type')
        desc_id = request.POST.get('element_desc_id')
        descriptor = current_data['click'][desc_id]

        check = element_id
        if group_id != desc_id:
            check = element_id[element_id.rfind(".")+1:]
        print check

        # remove node in click descriptor

        # (^\brt6\b\s*[\b\:\b]{2}\s*\w+\([\w\S\s]*?\)[^\/][^\/].*?;) #by clauz
        regex_node = "(^\\b"+check+"\\b\s*[\\b\:\\b]{2}\s*\w+\([\w\S\s]*?\)[^\/][^\/].*?;)"
        print regex_node
        regex_node_comp = re.compile(regex_node, flags=re.MULTILINE)
        descriptor = regex_node_comp.sub("", descriptor)

        # remove all links with source the node
        # (^\brt6\b\[[0-9]\][\w\S\s]*?;)
        #regex_node_src = "(^\\b"+check+"\\b\[[0-9]\][\w\S\s]*?;)"
        # (\bnds\b\[[0-9]+\][\w\s\S]*?;\s*?(?=\w)) #by clauz
        regex_node_src = "(^\\b" + check + "\\b\[[0-9]+\][\w\s\S]*?;\s*?(?=\w))"
        regex_node_src_comp = re.compile(regex_node_src, flags=re.MULTILINE)
        descriptor = regex_node_src_comp.sub("", descriptor)

        #remove all link with target the node


        print descriptor
        current_data['click'][desc_id] = descriptor
        self.data_project = current_data
        self.update()
        result = True
        return result

    # TODO modificare l'add_link
    def get_add_link(self, request):

        result = False
        current_data = json.loads(self.data_project)
        parameters = request.POST.dict()
        print "get_add_link", parameters

        group_id = request.POST.get('group_id')
        desc_id = request.POST.get('element_desc_id')
        source_id = request.POST.get('source')
        destination_id = request.POST.get('target')
        if group_id != desc_id:
            source_id = source_id[source_id.rfind(".") + 1:]
            destination_id = destination_id[destination_id.rfind(".") + 1:]
            lines = current_data['click'][desc_id].splitlines(True)
            for line in lines:
                if group_id + " ::" in line:
                    end = line.rfind("(") if line.rfind("(") != -1 else line.rfind(";")
                    element_class = line[line.rfind("::") + 2:end]
            for line in lines:
                check = element_class + " {"
                print check
                if check in line:
                    lines = lines[:lines.index(line) + 1] + [source_id + ' -> '+ destination_id + " ;\n"] + lines[lines.index(line) + 1:]
                    current_data['click'][desc_id] = ''.join(lines)
                    break
        else:
            current_data['click'][desc_id] += '\n '+ source_id + ' -> '+ destination_id+' ;'
        self.data_project = current_data
        self.update()
        result = True
        return result

    def get_remove_link(self, request):


        result = False
        current_data = json.loads(self.data_project)
        parameters = request.POST.dict()
        print "get_remove_link", parameters

        group_id = request.POST.get('group_id')
        desc_id = request.POST.get('element_desc_id')
        source_id = request.POST.get('source')
        destination_id = request.POST.get('target')
        descriptor = current_data['click'][desc_id]
        if group_id != desc_id:
            source_id = source_id[source_id.rfind(".") + 1:]
            destination_id = destination_id[destination_id.rfind(".") + 1:]

        # (\barp\b\[[0-9]+\][\w\s\S]*?\bto_eth0\b;\s*?(?=\w))
        regex_link = "(\\b"+source_id +"\\b\[[0-9]+\][\w\s\S]*?\\b"+destination_id+"\\b;\s*?(?=\w))"
        print regex_link
        regex_link_comp = re.compile(regex_link, flags=re.MULTILINE)
        descriptor = regex_link_comp.sub("", descriptor)

        current_data['click'][desc_id] = descriptor

        self.data_project = current_data
        self.update()
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
