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
    """Parser methods for etsi project type

    There is no actual parsing involved here, because the
    descriptor files are already JSON!
    """

    def __init__(self):
        super(ToscaParser, self).__init__()
    
    @classmethod        
    def importprojectdir(cls,dir_project, type):
        """Imports all files from NSD and VNFDs folders under a given folder

        this method is specific for Tosca project type
        """

        project = {
            'toscayaml': {},
            'positions': {}
        }
        # my_util = Util()
        NSD_PATH = dir_project+'/NSD'
        VNFD_PATH = dir_project+'/VNFD'

        #import network service description
        #in root directory file name nsd.json / nsd.yaml
        for nsd_filename in glob.glob(os.path.join(NSD_PATH, '*.json')):
            print nsd_filename
            nsd_object = Util.loadjsonfile(nsd_filename)
            project['nsd'][nsd_object['nsdIdentifier']] = nsd_object

        # import vnf descriptions
        # each file in root_path/VFND/*.json
        for vnfd_filename in glob.glob(os.path.join(VNFD_PATH, '*.json')):
            log.debug(vnfd_filename)
            vnfd_object = Util.loadjsonfile(vnfd_filename)
            project['vnfd'][vnfd_object['vnfdId']] = vnfd_object
        for vertices_file in glob.glob(os.path.join(dir_project, '*.json')):
            project['positions']['vertices'] = Util.loadjsonfile(vertices_file)

        #log.debug('\n' + json.dumps(project))
        return project

    @classmethod
    def importprojectfiles(cls, file_dict):
    # def importprojectfiles(cls,ns_files, vnf_files):
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
                toscajson = json.loads(Util.yaml2json(yaml_object))
                filename = os.path.splitext(os.path.basename(str(file)))[0]
                # project['toscayaml'][Util.get_unique_id()] = toscajson
                project['toscayaml'][filename] = toscajson

        return project

