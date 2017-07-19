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
import pyaml
import yaml

from lib.clickparser import click_parser
from lib.etsi.etsi_parser import EtsiParser
from lib.util import Util
from lib.parser import Parser
import logging
import traceback
import glob
import os

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('SuperfluidityParser')

class SuperfluidityParser(Parser):
    """Parser methods for superfluidity project type

    """

    def __init__(self):
        super(SuperfluidityParser, self).__init__()

    @classmethod
    def importprojectdir(cls,dir_project, file_type):
        """Imports all descriptor files under a given folder

        this method is specific for Superfluidity project type
        """

        project = {
            'nsd':{},

            'vnfd':{},

            'click':{},

            'k8s': {},

            'positions': {}
        }

        nfv_path = dir_project+"/NFV/"
        etsi_project = EtsiParser.importprojectdir( nfv_path + '/JSON', 'json')
        print etsi_project
        project['nsd'] = etsi_project['nsd']
        project['vnfd'] = etsi_project['vnfd']
        project['click'] = click_parser.importprojectdir(dir_project + '/CLICK/' , 'click')['click']
        # FIXME import k8s descriptors
        for k8s_filename in glob.glob(os.path.join(dir_project + '/K8S/', '*.yaml')):
            log.info(k8s_filename)
            yaml_object = Util().loadyamlfile(k8s_filename)
            json_object = Util.json_loads_byteified(Util.yaml2json(yaml_object))
            filename = os.path.splitext(os.path.basename(str(k8s_filename)))[0]
            project['k8s'][filename] = json_object

        for vertices_file in glob.glob(os.path.join(dir_project, '*.json')):
            if os.path.basename(vertices_file) == 'vertices.json':
                project['positions']['vertices'] = Util.loadjsonfile(vertices_file)

        print project

        return project

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
                    if(desc_type != 'k8s'):
                        project[desc_type][os.path.splitext(file.name)[0]] = json.loads(file.read())
                    else:
                        yaml_object = Util().loadyamlfile(file)
                        json_object = Util.json_loads_byteified(Util.yaml2json(yaml_object))
                        filename = os.path.splitext(os.path.basename(str(file)))[0]
                        project[desc_type][filename] = json_object

        return project

    def get_all_ns_descriptors(cls, nsd_id, project_data):
        vdu_type_map = {
            'kubernetes': 'k8s',
            'click': 'click'
        }
        try:
            descriptor = {
                'nsd': {},
                'vnfd': {},
                #'click': {},
                #'k8s': {}
            }
            #print nsd_id, project_data
            nsd_to_deploy = project_data['nsd'][nsd_id]
            descriptor['nsd'][nsd_id] = project_data['nsd'][nsd_id]
            for vnfdId in nsd_to_deploy['vnfdId']:
                descriptor['vnfd'][vnfdId] = project_data['vnfd'][vnfdId]
                for vdu in descriptor['vnfd'][vnfdId]['vdu']:
                    if 'vduNestedDescType' in vdu:
                        desc_type = vdu_type_map[str(vdu['vduNestedDescType'])] if str(vdu['vduNestedDescType']) in vdu_type_map else str(vdu['vduNestedDescType'])
                        if desc_type and vdu['vduNestedDesc'] and desc_type in project_data  \
                                and vdu['vduNestedDesc'] in project_data[desc_type]:
                            vduNestedDescType = str(vdu['vduNestedDescType'])
                            if vduNestedDescType not in descriptor:
                                descriptor[vduNestedDescType] = {}
                            print "vduNestedDescType", desc_type, vduNestedDescType, str(vdu['vduNestedDesc'])
                            descriptor[vduNestedDescType][str(vdu['vduNestedDesc'])] = project_data[desc_type][vdu['vduNestedDesc']]
        except Exception as e:
            print "Exception male male"
            log.exception(e)
            return {}

        return descriptor
