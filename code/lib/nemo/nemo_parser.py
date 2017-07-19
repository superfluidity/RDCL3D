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
log = logging.getLogger('NemoParser')

class NemoParser(Parser):
    """Parser methods for nemo project type

    """

    def __init__(self):
        super(NemoParser, self).__init__()
    
    @classmethod        
    def importprojectdir(cls,dir_project, file_type):
        """Imports all descriptor files under a given folder

        this method is specific for Nemo project type
        """

        project = {
            'intent':{},

            'nodemodel':{},

            'positions': {}
        }


        for desc_type in project:
            cur_type_path = os.path.join(dir_project, desc_type.upper())
            log.debug(cur_type_path)
            if os.path.isdir(cur_type_path):
                for file in glob.glob(os.path.join(cur_type_path, '*.'+file_type)):
                    if file_type == 'nemo':
                        project[desc_type][os.path.basename(file).split('.')[0]] = Util.openfile(file).read()

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
            'intent':{},

            'nodemodel':{},

        }
        print "Importing project file"
        for desc_type in project:
            if desc_type in file_dict:
                files_desc_type = file_dict[desc_type]
                for file in files_desc_type:
                    project[desc_type][os.path.splitext(file.name)[0]] = file.read()

        return project
