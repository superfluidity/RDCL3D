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

import yaml

from lib.util import Util
from lib.parser import Parser
import logging
import traceback
import glob
import os

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('EtsiParser')


class EtsiParser(Parser):
    """Parser methods for etsi project type

    There is no actual parsing involved here, because the
    descriptor files are already JSON!
    """

    def __init__(self):
        super(EtsiParser, self).__init__()
    
    @classmethod        
    def importprojectdir(cls,dir_project, file_type):
        """Imports all files from NSD and VNFDs folders under a given folder

        this method is specific for Etsi project type
        """

        project = {
            'nsd': {},
            'vnfd': {},
            'positions': {}
        }

        # my_util = Util()
        NSD_PATH = dir_project+'/NSD'
        VNFD_PATH = dir_project+'/VNFD'

        #import network service description
        #in root directory file name nsd.json / nsd.yaml
        for nsd_filename in glob.glob(os.path.join(NSD_PATH, '*.'+file_type)):
            log.debug(nsd_filename)
            nsd_object = Util.loadjsonfile(nsd_filename)
            project['nsd'][nsd_object['nsdIdentifier']] = nsd_object

        # import vnf descriptions
        # each file in root_path/VFND/*.json
        for vnfd_filename in glob.glob(os.path.join(VNFD_PATH, '*.'+file_type)):
            log.debug(vnfd_filename)
            vnfd_object = Util.loadjsonfile(vnfd_filename)
            project['vnfd'][vnfd_object['vnfdId']] = vnfd_object

        for vertices_file in glob.glob(os.path.join(dir_project, '*.json')):
            if os.path.basename(vertices_file) == 'vertices.json':
                project['positions']['vertices'] = Util.loadjsonfile(vertices_file)

        return project

    @classmethod
    def importprojectfiles(cls, file_dict):
        """Imports descriptors (extracted from the new project POST)

        The keys in the dictionary are the file types
        """
        project = {
            'nsd': {},
            'vnfd': {}
        }

        for desc_type in project:
            key_file = desc_type+'_files'
            if key_file in file_dict:
                files_desc_type = file_dict[key_file]
                for file in files_desc_type:
                    project[desc_type][os.path.splitext(file.name)[0]] = cls.descriptortojson(file.read())
        return project

    @classmethod
    def descriptortojson(cls, descriptor_string):

        try:
            json_object = json.load(descriptor_string)
            return json_object
        except Exception as e:
            log.debug('The String is not JSON')
        try:
            yaml_object = yaml.load(descriptor_string)
            return yaml_object
        except:
            log.debug('The String is not YAML')
            raise Exception('The Etsi descriptor is not a valid JSON/YAML file')

