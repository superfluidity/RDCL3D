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

import json
from lib.clickparser import click_parser
from lib.etsi.etsi_parser import EtsiParser
from lib.util import Util
from lib.parser import Parser
import logging
import glob
import os

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('SuperfluidityParser')


class SuperfluidityParser(Parser):
    """Parser methods for superfluidity project type

    """

    vdu_type_map = {
        'kubernetes': 'k8s',
        'click': 'click',
        'docker': 'docker',
        'ansibledocker': 'ansibledocker'
    }

    def __init__(self):
        super(SuperfluidityParser, self).__init__()

    @classmethod
    def importprojectdir(cls, dir_project, file_type):
        """Imports all descriptor files under a given folder

        this method is specific for Superfluidity project type
        """

        project = {
            'nsd': {},

            'vnfd': {},

            'click': {},

            'k8s': {},

            'resource': {},

            'positions': {}
        }

        nfv_path = dir_project + "/NFV/"
        etsi_project = EtsiParser.importprojectdir(nfv_path + '/JSON', 'json')
        #print etsi_project
        project['nsd'] = etsi_project['nsd']
        project['vnfd'] = etsi_project['vnfd']
        project['click'] = click_parser.importprojectdir(dir_project + '/CLICK/', 'click')['click']
        # FIXME import k8s descriptors
        project['k8s'] = cls.import_kubernetes_from_dir_project(dir_project)

        for vertices_file in glob.glob(os.path.join(dir_project, '*.json')):
            if os.path.basename(vertices_file) == 'vertices.json':
                project['positions']['vertices'] = Util.loadjsonfile(vertices_file)

        #print project

        return project

    @classmethod
    def import_kubernetes_from_dir_project(cls, dir_project):
        result = {}
        for k8s_filename in glob.glob(os.path.join(dir_project, 'K8S', '*.yaml')):
            log.info(k8s_filename)
            yaml_object = Util().loadyamlfile(k8s_filename)
            json_object = Util.json_loads_byteified(Util.yaml2json(yaml_object))
            filename = os.path.splitext(os.path.basename(str(k8s_filename)))[0]
            result[filename] = json_object
        return result

    @classmethod
    def importprojectfiles(cls, file_dict):
        """Imports descriptors (extracted from the new project POST)

        The keys in the dictionary are the file types
        """
        project = {
            'nsd': {},

            'vnfd': {},

            'click': {},

            'k8s': {}

        }
        for desc_type in project:
            if desc_type in file_dict:
                files_desc_type = file_dict[desc_type]
                for file in files_desc_type:
                    if desc_type != 'k8s':
                        project[desc_type][os.path.splitext(file.name)[0]] = json.loads(file.read())
                    else:
                        yaml_object = Util().loadyamlfile(file)
                        json_object = Util.json_loads_byteified(Util.yaml2json(yaml_object))
                        filename = os.path.splitext(os.path.basename(str(file)))[0]
                        project[desc_type][filename] = json_object

        return project

    def get_all_ns_descriptors(cls, nsd_id, project_data):

        try:
            descriptor = {
                'nsd': {},
                'vnfd': {},
                # 'click': {},
                # 'k8s': {}
            }
            # print nsd_id, project_data
            nsd_to_deploy = project_data['nsd'][nsd_id]
            descriptor['nsd'][nsd_id] = project_data['nsd'][nsd_id]
            for vnfdId in nsd_to_deploy['vnfdId']:
                descriptor['vnfd'][vnfdId] = project_data['vnfd'][vnfdId]
                for vdu in descriptor['vnfd'][vnfdId]['vdu']:
                    if 'vduNestedDesc' in vdu:
                        vdu_nested_desc = vdu['vduNestedDesc']
                        descriptor.update(
                            cls.get_nested_vdu_descriptor(vdu_nested_desc, project_data['vnfd'][vnfdId], project_data))
        except Exception as e:
            print "Exception male male"
            log.exception(e)
            return {}

        return descriptor

    def get_nested_vdu_descriptor(cls, nested_vdu_id, vnf_data, project_data):
        result = {}
        try:
            nested_vdu = cls.get_nested_vdu_from_id(nested_vdu_id,vnf_data)
            if nested_vdu:
                vdu_nested_desc_type = cls.vdu_type_map[nested_vdu['vduNestedDescriptorType']]
                vdu_nested_descriptor = nested_vdu['vduNestedDescriptor']
                if vdu_nested_desc_type not in result:
                    result[vdu_nested_desc_type] = {}
                print 'get_nested_vdu_descriptor', vdu_nested_desc_type, vdu_nested_descriptor
                if vdu_nested_desc_type in project_data and vdu_nested_descriptor in project_data[vdu_nested_desc_type]:
                    print vdu_nested_desc_type, vdu_nested_descriptor
                    result[vdu_nested_desc_type][vdu_nested_descriptor] = project_data[vdu_nested_desc_type][vdu_nested_descriptor]
        except Exception as e:
            log.exception(e)
            return {}
        print 'result', result
        return result

    @staticmethod
    def get_nested_vdu_from_id(nested_vdu_id, vnf_data):
        try:

            for nested_vdu in vnf_data['vduNestedDesc']:
                if nested_vdu['id'] == nested_vdu_id:
                    return nested_vdu
        except Exception as e:
            log.exception(e)
        return None

    @staticmethod
    def find_object_from_list(key, value, data_dict, key_list):
        try:
            for item in data_dict[key_list]:
                if item[key] == value:
                    return item
        except Exception as e:
            log.exception(e)
        return None
