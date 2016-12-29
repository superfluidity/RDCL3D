import json
import pyaml
import yaml
from lib.util import Util
from lib.etsi.etsi_rdcl_graph import EtsiRdclGraph
from lib.etsi.etsi_parser import EtsiParser
import logging
import traceback
import glob
import os

''' 
TODO(stefano) I have created this module to clean up etsi_parser.py
may be it can be deleted 
'''


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('Main_EtsiParser')


if __name__ == '__main__':

    # test = Util()
    test_rdcl = EtsiRdclGraph()

    #yaml_object = yaml.load(yaml_string)
    #log.debug(yaml_string)
    #json_object = test.yaml2json(yaml_object)
    #log.debug(json_object)
    try:
        #importProject('../../sf_dev/examples/my_example/JSON', 'json')

        #importproject() needs to be replaced with some method from EtsiParser
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