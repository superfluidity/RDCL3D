#
#   Copyright 2017 CNIT - Consorzio Nazionale Interuniversitario per le Telecomunicazioni
#
#   Licensed under the Apache License, Version 2.0 (the );
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

            'positions': {}
        }
        nfv_path = dir_project+"/NFV/"
        etsi_project = EtsiParser.importprojectdir( nfv_path + '/JSON', 'json')
        print etsi_project
        project['nsd'] = etsi_project['nsd']
        project['vnfd'] = etsi_project['vnfd']
        project['click'] = click_parser.importprojectdir(dir_project + '/CLICK/' , 'click')['click']


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
            'nsd':{},

            'vnfd':{},

            'click':{},

        }
        for desc_type in project:
            if desc_type in file_dict:
                files_desc_type = file_dict[desc_type]
                for file in files_desc_type:
                    project[desc_type][os.path.splitext(file.name)[0]] = json.loads(file.read())

        return project
