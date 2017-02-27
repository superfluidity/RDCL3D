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
from lib.util import Util
from lib.parser import Parser
import logging
import traceback
import glob
import os



logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('ToscaParser')

class ToscaParser(Parser):
    """Parser methods for tosca project type


    """

    def __init__(self):
        super(ToscaParser, self).__init__()
    
    @classmethod        
    def importprojectdir(cls,dir_project, type):
        """Imports all files under a given folder

        This method is specific for Tosca project type
        """

        project = {
            'toscayaml': {},
            'positions': {}
        }
        for file in glob.glob(os.path.join(dir_project, '*.yaml')):

            yaml_object =  Util().loadyamlfile(file)
            #toscajson = json.loads(Util.yaml2json(yaml_object))
            toscajson = Util.json_loads_byteified(Util.yaml2json(yaml_object))
            filename = os.path.splitext(os.path.basename(str(file)))[0]
            # project['toscayaml'][Util.get_unique_id()] = toscajson
            if filename == 'vertices':
                project['positions'] = toscajson
            else:
                project['toscayaml'][filename] = toscajson


        #log.debug('\n' + json.dumps(project))
        return project

    @classmethod
    def importprojectfiles(cls, file_dict):
        """Imports descriptors (extracted from the new project POST)

        The keys in the file dictionary are the file types
        """
        project = {
            'toscayaml': {}
        }

        if 'toscayaml_files' in file_dict:
            tmp_files = file_dict['toscayaml_files']
            for file in tmp_files:

                yaml_object = yaml.load(file)
                #toscajson = json.loads(Util.yaml2json(yaml_object))
                toscajson = Util.json_loads_byteified(Util.yaml2json(yaml_object))
                filename = os.path.splitext(os.path.basename(str(file)))[0]
                # project['toscayaml'][Util.get_unique_id()] = toscajson
                project['toscayaml'][filename] = toscajson

        return project

