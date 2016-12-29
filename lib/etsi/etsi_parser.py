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
log = logging.getLogger('EtsiParser')

class EtsiParser(Parser):
    """Parser methods for etsi project type

    There is no actual parsing involved here, because the
    descriptor files are already JSON!
    """

    def __init__(self):
        super(EtsiParser, self).__init__()
    
    @classmethod        
    def importprojectdir(cls,dir_project, type):
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
    def importprojectfile(cls,ns_files, vnf_files):
        """Imports an array of NS files and an array of VNF files

        this method is specific for Etsi project type
        """
        project = {
            'nsd': {},
            'vnfd': {}
        }
        for file in ns_files:
            nsd =json.loads(file.read())
            project['nsd'][nsd['nsdIdentifier']] = nsd
        for file in vnf_files:
            vnf =json.loads(file.read())
            project['vnfd'][vnf['vnfdId']] = vnf
        return project

