import json
import pyaml
import yaml
from util import Util
from rdcl3d_util import Rdcl3d_util
import logging
import traceback
import glob
import os

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('EmpLogger')


def importprojectdir(dir_project, type):
    '''Imports all files from NSD and VNFDs folders under a given folder

    NB: currently, this method is specific for Etsi project type
    '''

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

def importprojectfile(ns_files, vnf_files):
    '''Imports an array of NS files and an array of VNF files

    NB: currently, this method is specific for Etsi project type
    '''
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


if __name__ == '__main__':

    # test = Util()
    test_rdcl = Rdcl3d_util()

    #yaml_object = yaml.load(yaml_string)
    #log.debug(yaml_string)
    #json_object = test.yaml2json(yaml_object)
    #log.debug(json_object)
    try:
        #importProject('../../sf_dev/examples/my_example/JSON', 'json')
        project = importproject('/Users/francesco/Workspace/sf_t3d/sf_dev/examples/my_example/JSON', 'json')
        topology = test_rdcl.build_graph_from_project(project)
        Util.writejsonfile('/Users/francesco/Workspace/sf_t3d/sf_dev/examples/my_example/JSON/t3d.json', topology)

        # json_object_from_file = test.loadjsonfile('../../sf_dev/examples/my_example/JSON/nsd.json')
        # test.writeyamlfile('../../sf_dev/examples/my_example/YAML/nsd.yaml', json_object_from_file)
        # json_object_from_file = test.loadjsonfile('../../sf_dev/examples/my_example/JSON/VNFD/vnf1.json')
        # test.writeyamlfile('../../sf_dev/examples/my_example/YAML/VNFD/vnf1.yaml', json_object_from_file)
        # json_object_from_file = test.loadjsonfile('../../sf_dev/examples/my_example/JSON/VNFD/vnf2.json')
        # test.writeyamlfile('../../sf_dev/examples/my_example/YAML/VNFD/vnf2.yaml', json_object_from_file)
        # json_object_from_file = test.loadjsonfile('../../sf_dev/examples/my_example/JSON/VNFD/vnf3.json')
        # test.writeyamlfile('../../sf_dev/examples/my_example/YAML/VNFD/vnf3.yaml', json_object_from_file)
        # json_object_from_file = test.loadjsonfile('../../sf_dev/examples/my_example/JSON/VLD/vl1.json')
        # test.writeyamlfile('../../sf_dev/examples/my_example/YAML/VLD/vl1.yaml', json_object_from_file)
        # json_object_from_file = test.loadjsonfile('../../sf_dev/examples/my_example/JSON/VLD/vl2.json')
        # test.writeyamlfile('../../sf_dev/examples/my_example/YAML/VLD/vl2.yaml', json_object_from_file)
        # json_object_from_file = test.loadjsonfile('../../sf_dev/examples/my_example/JSON/VLD/vl3.json')
        # test.writeyamlfile('../../sf_dev/examples/my_example/YAML/VLD/vl3.yaml', json_object_from_file)
        # json_object_from_file = test.loadjsonfile('../../sf_dev/examples/my_example/JSON/VLD/vl4.json')
        # test.writeyamlfile('../../sf_dev/examples/my_example/YAML/VLD/vl4.yaml', json_object_from_file)

        #log.debug(json_object_from_file)
        #json_object_from_file = test.loadjsonfile('../../sf_dev/examples/nsd_oimsc_unique/nsd.json')
        #yaml_object_from_file = test.loadyamlfile('../../sf_dev/examples/nsd_iperf_cs/nsd.yaml')
        #log.debug(pyaml.dump(yaml_object_from_file))
        #test.writeyamlfile('../../sf_dev/examples/nsd_iperf_cs/nsd_test.yaml', yaml_object_from_file)
        #test.writejsonfile('../../sf_dev/examples/nsd_iperf_cs/nsd_test.json', test_rdcl.build_graph_from_baton((json_object_from_file)))
    except IOError as e:
        #log.error('Error test')
        traceback.print_exc()