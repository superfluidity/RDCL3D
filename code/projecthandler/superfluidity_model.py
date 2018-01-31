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
from lib.superfluidity.sf_ansible import AnsibleUtility
from sf2heat.nsdtranslator import NSDTranslator

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('SuperfluidityModel.py')

PATH_TO_SCHEMAS = 'lib/superfluidity/schemas/'
PATH_TO_DESCRIPTORS_TEMPLATES = 'lib/superfluidity/descriptor_template'
DESCRIPTOR_TEMPLATE_SUFFIX = '.json'
GRAPH_MODEL_FULL_NAME = 'lib/TopologyModels/superfluidity/superfluidity.yaml'
EXAMPLES_FOLDER = 'usecases/SUPERFLUIDITY/'

etsi_elements = ['ns_cp', 'ns_vl', 'vnf', 'vnf_vl', 'vnf_ext_cp', 'vnf_vdu', 'vnf_vdu_cp', 'vnffg']
sf_elements = ['vnf_click_vdu', 'vnf_k8s_vdu', 'vnf_docker_vdu', 'vnf_ansibledocker_vdu', 'k8s_service_cp']
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
            if type_descriptor != "resource":
                schema = Util.loadjsonfile(
                    os.path.join(PATH_TO_DESCRIPTORS_TEMPLATES, type_descriptor + DESCRIPTOR_TEMPLATE_SUFFIX))
            else:
                schema = ""
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
            'resource': len(current_data['resource'].keys()) if 'resource' in current_data else 0,
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
            elif data_type == 'k8s':
                new_descriptor = new_data
            elif data_type == 'resource':
                new_descriptor = new_data
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
        if element_type in etsi_elements:
            result = EtsiProject.get_add_element(self, request)
        elif element_type in sf_elements:
            vnf_id = request.POST.get('group_id')
            element_id = request.POST.get('element_id')
            opt_params = request.POST.get('opt_params')
            if 'opt_params' in parameters:
                print parameters['opt_params']
                opt_params = json.loads(opt_params)
            if element_type == 'vnf_click_vdu' or element_type == 'vnf_k8s_vdu' or element_type == 'vnf_ansibledocker_vdu':
                result = self.add_vnf_nested_vdu(vnf_id, element_id, **opt_params)
            elif element_type == 'vnf_docker_vdu':
                result = self.add_vnf_docker_vdu(vnf_id, element_id, **opt_params)
            elif element_type == 'k8s_service_cp':
                result = self.add_k8s_service_cp(vnf_id, element_id, **opt_params)
        elif element_type in click_elements:
            result = ClickProject.get_add_element(self, request)

        return result

    def get_remove_element(self, request):
        result = False
        parameters = request.POST.dict()
        element_type = request.POST.get('element_type')

        if element_type in etsi_elements:
            result = EtsiProject.get_remove_element(self, request)
        elif element_type in sf_elements:
            group_id = request.POST.get('group_id')
            element_id = request.POST.get('element_id')
            if element_type == 'vnf_k8s_vdu' or element_type == 'vnf_click_vdu' or element_type == 'vnf_docker_vdu':
                result = EtsiProject.remove_vnf_vdu(self, group_id, element_id)
            if element_type == 'k8s_service_cp':
                result = self.remove_k8s_service_cp(group_id, element_id)

        elif element_type in click_elements:
            result = ClickProject.get_remove_element(self, request)

        return result

    def get_node_overview(self, **kwargs):
        """Returns the node overview"""
        element_type = kwargs['element_type']
        # print kwargs
        if element_type == 'vnf':
            return self._vnf_overview(**kwargs)
        return {}

    def _vnf_overview(self, **kwargs):
        result = {
            'vdu': []
        }
        # FIXME adattare a nuovo descrittore
        descriptor = self.get_descriptor(kwargs['element_id'], 'vnfd')
        for vdu in descriptor['vdu']:
            current = {
                "vduId": vdu['vduId'],
                "type": vdu['vduNestedDescType'] if 'vduNestedDescType' in vdu else 'default (full VM)',
                "source": vdu['vduNestedDesc'] if 'vduNestedDesc' in vdu else (vdu['swImageDesc']['swImage'])
            }
            result['vdu'].append(current)
        return result

    def get_add_link(self, request):
        result = False
        parameters = request.POST.dict()

        source_type = parameters['source_type']
        destination_type = parameters['target_type']

        if source_type in etsi_elements and destination_type in etsi_elements:
            result = EtsiProject.get_add_link(self, request)
        elif source_type in click_elements and destination_type in click_elements:
            result = ClickProject.get_add_link(self, request)
        elif source_type in sf_elements and destination_type in sf_elements:
            if (source_type, destination_type) in [('vnf_k8s_vdu', 'k8s_service_cp'), ('k8s_service_cp', 'vnf_k8s_vdu')]:
                result = self.link_k8sscp_k8_vdu(parameters)
            else:
                result = False

        return result

    def get_remove_link(self, request):

        result = False
        parameters = request.POST.dict()
        source_type = parameters['source_type']
        destination_type = parameters['target_type']

        if source_type in etsi_elements and destination_type in etsi_elements:
            result = EtsiProject.get_remove_link(self, request)
        elif source_type in sf_elements and destination_type in sf_elements:
            if (source_type, destination_type) in [('vnf_k8s_vdu', 'k8s_service_cp'), ('k8s_service_cp', 'vnf_k8s_vdu')]:
                result = self.unlink_k8sscp_k8_vdu(parameters)

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

    def add_vnf_nested_vdu(self, vnf_id, vdu_id, **kwargs):
        log.debug('add_vnf_nested_vdu')
        try:
            log.debug(kwargs['nested_desc']['id'])
            current_data = json.loads(self.data_project)
            vdu_descriptor = self.get_descriptor_template('vnfd')['vdu'][0]
            vdu_descriptor['vduId'] = vdu_id
            vdu_descriptor['intCpd'] = []
            vdu_descriptor['vduNestedDesc'] = kwargs['nested_desc']['id']

            if 'vdu_param' in kwargs:
                vdu_descriptor.update(kwargs['vdu_param'])

            vdu_nested_desc = self.get_descriptor_template('vdunesteddesc')

            vdu_nested_desc.update(kwargs['nested_desc'])
            current_data['vnfd'][vnf_id]['vdu'].append(vdu_descriptor)
            current_data['vnfd'][vnf_id] = self._append_vdu_nested_desc(vdu_nested_desc, current_data['vnfd'][vnf_id])

            self.data_project = current_data
            self.update()
            result = True
        except Exception as e:
            log.exception(e)
            result = False
        return result

    def add_vnf_docker_vdu(self, vnf_id, vdu_id, **kwargs):
        log.debug('add_vnf_docker_vdu')
        try:
            current_data = json.loads(self.data_project)
            if 'docker_image_name' in kwargs:
                vdu_descriptor = self.get_descriptor_template('vdu_docker_image')
                vdu_descriptor['swImageDesc']['id'] = kwargs['docker_image_name']
                if 'envVar' in kwargs:
                    vdu_descriptor['swImageDesc']['envVars'] = kwargs['envVar']
            elif 'docker_file_name' in kwargs:
                vdu_descriptor = self.get_descriptor_template('vdu_with_nested_desc')
                if 'envVars' in kwargs:
                    vdu_descriptor['envVars'] = kwargs['envVars']
            else:
                return False
            vdu_descriptor['vduId'] = vdu_id
            current_data['vnfd'][vnf_id]['vdu'].append(vdu_descriptor)
            self.data_project = current_data
            self.update()
            result = True
        except Exception as e:
            log.exception(e)
            result = False
        return result


    def add_k8s_service_cp(self, vnf_id, element_id, **kwargs):
        log.debug('add_k8s_service_cp')
        try:
            current_data = json.loads(self.data_project)
            k8s_service_cp = self.get_descriptor_template('k8sservicecpd')
            k8s_service_cp.update(kwargs['k8s_service_cpd'])
            vnf = current_data['vnfd'][vnf_id]
            if 'k8SServiceCpd' not in vnf:
                vnf['k8SServiceCpd'] = []
            if SuperfluidityParser.find_object_from_list('cpdId', element_id, vnf, 'k8SServiceCpd') is None:
                vnf['k8SServiceCpd'].append(k8s_service_cp)


            self.data_project = current_data
            self.update()
            result = True
        except Exception as e:
            log.exception(e)
            result = False
        return result

    def remove_k8s_service_cp(self, vnf_id, element_id):
        log.debug('remove_k8s_service_cp')
        try:
            current_data = json.loads(self.data_project)
            vnf = current_data['vnfd'][vnf_id]
            k8s_service_cp = next((x for x in vnf['k8SServiceCpd'] if x['cpdId'] == element_id), None)
            if k8s_service_cp is not None:
                vnf['k8SServiceCpd'].remove(k8s_service_cp)

            self.data_project = current_data
            self.update()
            result = True
        except Exception as e:
            log.exception(e)
            result = False
        return result

    def link_k8sscp_k8_vdu(self, link_data):
        try:
            current_data = json.loads(self.data_project)
            vnf_id = link_data['group_id']
            k8vdu_id = link_data['source'] if link_data['source_type'] == 'vnf_k8s_vdu' else link_data['target']
            k8s_service_cp_id = link_data['source'] if link_data['source_type'] == 'k8s_service_cp' else link_data['target']
            #k8_vdu_descriptor = next((x for x in current_data['vnfd'][vnf_id]['vdu'] if x['vduId'] == k8vdu_id), None)
            k8s_service_cp_descriptor = next((x for x in current_data['vnfd'][vnf_id]['k8SServiceCpd'] if x['cpdId'] == k8s_service_cp_id), None)
            if k8vdu_id not in k8s_service_cp_descriptor['exposedPod']:
                k8s_service_cp_descriptor['exposedPod'].append(k8vdu_id)
            self.data_project = current_data
            self.update()
            result = True
        except Exception as e:
            log.exception(e)
            result = False
        return result

    def unlink_k8sscp_k8_vdu(self, link_data):
        try:
            current_data = json.loads(self.data_project)
            vnf_id = link_data['group_id']
            k8vdu_id = link_data['source'] if link_data['source_type'] == 'vnf_k8s_vdu' else link_data['target']
            k8s_service_cp_id = link_data['source'] if link_data['source_type'] == 'k8s_service_cp' else link_data['target']
            print k8s_service_cp_id, k8vdu_id, link_data['source'], link_data['target']
            k8s_service_cp_descriptor = next(
                (x for x in current_data['vnfd'][vnf_id]['k8SServiceCpd'] if x['cpdId'] == k8s_service_cp_id), None)
            print "k8s_service_cp_descriptor", k8s_service_cp_descriptor
            if k8vdu_id in k8s_service_cp_descriptor['exposedPod']:
                k8s_service_cp_descriptor['exposedPod'].remove(k8vdu_id)
            self.data_project = current_data
            self.update()
            result = True
        except Exception as e:
            log.exception(e)
            result = False
        return result

    def _append_vdu_nested_desc(self, nested_data, vnf):
        if 'vduNestedDesc' not in vnf:
            vnf['vduNestedDesc'] = []
        if SuperfluidityParser.get_nested_vdu_from_id(nested_data['id'], vnf) is None:
            vnf['vduNestedDesc'].append(nested_data)
        return vnf

    def get_available_nodes(self, args):
        """Returns all available node """
        log.debug('get_available_nodes')
        try:
            result = []
            categories = {}
            # current_data = json.loads(self.data_project)
            model_graph = self.get_graph_model(GRAPH_MODEL_FULL_NAME)
            if args['layer'] in model_graph['layer']:
                for node in model_graph['layer'][args['layer']]['nodes']:
                    if 'addable' in model_graph['layer'][args['layer']]['nodes'][node] and \
                            model_graph['layer'][args['layer']]['nodes'][node]['addable']:
                        category_name = model_graph['nodes'][node]['type'] if 'type' in model_graph['nodes'][node] else \
                        model_graph['nodes'][node]
                        if category_name not in categories:
                            categories[category_name] = {
                                "category_name": category_name,
                                "types": []
                            }
                        categories[category_name]["types"].append({
                            "name": model_graph['nodes'][node]['label'],
                            "id": node
                        })
                    # result.append(current_data)
            result = categories.values()
            # result = current_data[type_descriptor][descriptor_id]
        except Exception as e:
            log.exception(e)
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
                        zip.writestr(current_desc + '.yaml', yaml.safe_dump(current_data[desc_type][current_desc]))
                    else:
                        zip.writestr(current_desc + '.json', json.dumps(current_data[desc_type][current_desc]))

            zip.close()
        except Exception as e:
            log.exception(e)

        in_memory.flush()
        return in_memory

    def get_all_ns_descriptors(self, nsd_id):
        sf_parser = SuperfluidityParser()
        result = sf_parser.get_all_ns_descriptors(nsd_id, json.loads(self.data_project))
        return result

    def translate_push_ns_on_repository(self, translator, nsd_id, repository, **kwargs):
        ns_data = self.get_all_ns_descriptors(nsd_id)
        if translator == 'k8sansible':
            ansible_util = AnsibleUtility()
            playbooks_path = kwargs['repo_path'] + '/project_' + str(self.id) + '/' + nsd_id + '/'
            conversion_report = ansible_util.generate_playbook(ns_data, nsd_id, playbooks_path)

        elif translator == 'sf2heat':
            hot_path = kwargs['repo_path'] + '/project_' + str(self.id) + '/' + nsd_id + '_hot'
            if not os.path.isdir(hot_path):
                os.makedirs(hot_path)
            nsd_translator = NSDTranslator(ns_data, hot_path, {'app_name': nsd_id, 'cloud_config_name': nsd_id+ str(self.id)})
            nsd_translator.translate()
        commit_msg = kwargs['commit_msg'] if (
        'commit_msg' in kwargs and kwargs['commit_msg'] != '') else 'update project_' + str(self.id) + ' nsd:' + nsd_id
        push_result = repository.push_repository(msg=commit_msg)
        return push_result


