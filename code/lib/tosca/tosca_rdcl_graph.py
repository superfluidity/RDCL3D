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
import logging
import copy
import six
from lib.rdcl_graph import RdclGraph

from toscaparser.tosca_template import ToscaTemplate
from translator.hot.tosca_translator import TOSCATranslator

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('ToscaRdclGraph')

class ToscaRdclGraph(RdclGraph):
    """Operates on the graph representation used for the GUI graph views"""

    def __init__(self):
        pass


    def build_graph_from_project(self, json_project, model={}):
        """Creates a single graph for a whole project

        json_project is the dict representation of the project
        """

        #print "json_project ",json_project
        graph_object = {
            'vertices': [],
            'edges': [],
            'graph_parameters': {},
            'model': model
        }
        try:
            positions = json_project['positions'] if 'positions' in json_project else False
            log.debug('build graph from project json')

            # print json.dumps(json_project, sort_keys=True, indent=4, separators=(',', ': '))
            # print json_project['toscayaml']
            # print json.dumps(json_project['toscayaml'], sort_keys=True, indent=4, separators=(',', ': '))

            #path = '/home/user/RDCL/heat-translator/translator/tests/data/network/tosca_two_servers_one_network.yaml'
            # tosca = ToscaTemplate(path, parsed_params, a_file)

            for toscayaml_name in json_project['toscayaml'].keys():
                print ("\ntoscayaml_name: "+toscayaml_name)

                #tosca = ToscaTemplate('/home/kaarot_kalel_90/PycharmProjects/test-rdcl/code/usecases/TOSCA/Sample-tosca-nfv/YAML/ns.yaml')
                tosca = ToscaTemplate(None, {}, False, yaml_dict_tpl=json_project['toscayaml'][toscayaml_name], project = json_project['toscayaml'])
                #tosca = TOSCATranslator('/home/kaarot_kalel_90/PycharmProjects/test-rdcl/code/usecases/TOSCA/Sample-tosca-nfv/YAML/ns.yaml',{})

                version = tosca.version
                if tosca.version:
                    print("\nversion: " + version)

                if hasattr(tosca, 'description'):
                    description = tosca.description
                    if description:
                        print("\ndescription: " + description)

                if hasattr(tosca, 'inputs'):
                    inputs = tosca.inputs
                    if inputs:
                        print("\ninputs:")
                        for input in inputs:
                            print("\t" + input.name)

                if hasattr(tosca, 'nodetemplates'):
                    nodetemplates = tosca.nodetemplates
                    if nodetemplates:
                        print("\nnodetemplates:")
                        for node in nodetemplates:
                            print("\t" + node.name)

                if hasattr(tosca, 'outputs'):
                    outputs = tosca.outputs
                    if outputs:
                        print("\noutputs:")
                        for output in outputs:
                            print("\t" + output.name)


                if hasattr(tosca, 'graph'):
                    # For the moment, we consider a single view called 'graph'
                    #print tosca.nested_tosca_tpls_with_topology
                    for node in tosca.graph.nodetemplates:
                        #print dir(node)
                        #print node.type
                        #print node.name+" is derived from0 "+ node.parent_type.type
                        if node.name in tosca.graph.vertices:
                            print 'node '+node.name+' is related to:'
                            # self.add_node(node.name, node.type, 'vnf', positions, graph_object)
                            #def add_node(id,        type,      group,          positions, graph_object):
                            self.add_node(node.name, node.type, toscayaml_name, positions, graph_object)
                            related = tosca.graph.vertex(node.name).related_nodes
                            for related_node in related:
                                print related_node.name + '->' + tosca.graph.vertex(node.name).related[related_node].type

                                #def add_link(source,    target,            view,    group,       graph_object )
                                self.add_link(node.name, related_node.name, 'graph', toscayaml_name, graph_object)
                else :
                    log.debug('tosca template has no graph')

                # #THIS IS FOR THE TRANSLATION INTO HOT TEMPLATES
                # translator = TOSCATranslator(tosca, {}, False,
                #                              csar_dir=None)
                # yaml_files = translator.output_to_yaml_files_dict('output.yaml')
                # for name, content in six.iteritems(yaml_files):
                #     if name != "output.yaml":
                #         with open(name, 'w+') as f:
                #             f.write(content)
                # print(yaml_files['output.yaml'])

        except Exception as e:
            print e
            log.error('Exception in build_graph_from_project')
            raise

        return graph_object

