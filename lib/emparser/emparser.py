import json
import pyaml
import yaml
from util import Util
from t3d_util import T3DUtil
import logging
import traceback
import glob
import os

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('EmpLogger')


def importproject(dir_project, type):
    project = {
        'nsd': {},
        'vld': {},
        'vnfd': {}
    }
    my_util = Util()
    VLD_PATH = dir_project+'/VLD'
    VNFD_PATH = dir_project+'/VNFD'

    #import network service description
    #in root directory file name nsd.json / nsd.yaml
    nsd_object = my_util.loadjsonfile(dir_project+'/nsd.json')
    project['nsd'] = nsd_object

    #import virtual link descriptions
    #each file in root_path/VLD/*.json

    for vld_filename in glob.glob(os.path.join(VLD_PATH, '*.json')):
        #log.debug(vld_filename)
        vld_object = my_util.loadjsonfile(vld_filename)
        project['vld'][vld_object['id']]= vld_object

    # import vnf descriptions
    # each file in root_path/VFND/*.json
    for vnfd_filename in glob.glob(os.path.join(VNFD_PATH, '*.json')):
        log.debug(vnfd_filename)
        vnfd_object = my_util.loadjsonfile(vnfd_filename)
        project['vnfd'][vnfd_object['id']] = vnfd_object

    #log.debug('\n' + json.dumps(project))
    return project


if __name__ == '__main__':

    test = Util()
    test_t3d = T3DUtil()

    #yaml_object = yaml.load(yaml_string)
    #log.debug(yaml_string)
    #json_object = test.yaml2json(yaml_object)
    #log.debug(json_object)
    try:
        #importProject('../../sf_dev/examples/my_example/JSON', 'json')
        project = importproject('/Users/francesco/Workspace/sf_t3d/sf_dev/examples/my_example/JSON', 'json')
        topology = test_t3d.build_graph_from_project(project)
        #json_object_from_file = test.loadjsonfile('../../sf_dev/examples/my_example/JSON/nsd_example.json')
        #log.debug(json_object_from_file)
        #json_object_from_file = test.loadjsonfile('../../sf_dev/examples/nsd_oimsc_unique/nsd.json')
        #yaml_object_from_file = test.loadyamlfile('../../sf_dev/examples/nsd_iperf_cs/nsd.yaml')
        #log.debug(pyaml.dump(yaml_object_from_file))
        #test.writeyamlfile('../../sf_dev/examples/nsd_iperf_cs/nsd_test.yaml', yaml_object_from_file)
        #test.writejsonfile('../../sf_dev/examples/nsd_iperf_cs/nsd_test.json', test_t3d.build_graph_from_baton((json_object_from_file)))
    except IOError as e:
        #log.error('Error test')
        traceback.print_exc()