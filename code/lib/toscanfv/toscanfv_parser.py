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
log = logging.getLogger('ToscanfvParser')

class ToscanfvParser(Parser):
    """Parser methods for toscanfv project type

    """

    def __init__(self):
        super(ToscanfvParser, self).__init__()
    
    @classmethod        
    def importprojectdir(cls,dir_project, file_type):
        """Imports all descriptor files under a given folder

        this method is specific for Toscanfv project type
        """

        project = {
            'toscayaml':{},

            'positions': {}
        }


        for desc_type in project:
            cur_type_path = os.path.join(dir_project, desc_type.upper())
            log.debug(cur_type_path)
            if os.path.isdir(cur_type_path):
                for file in glob.glob(os.path.join(cur_type_path, '*.'+file_type)):
                    if file_type == 'json':
                        project[desc_type][os.path.basename(file).split('.')[0]] = Util.loadjsonfile(file)
                    elif file_type == 'yaml':
                        project[desc_type][os.path.basename(file).split('.')[0]] = Util.loadyamlfile(file)


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
            'toscayaml':{},

        }
        for desc_type in project:
            if desc_type in file_dict:
                files_desc_type = file_dict[desc_type]
                for file in files_desc_type:
                    project[desc_type][os.path.splitext(file.name)[0]] = json.loads(file.read())

        return project