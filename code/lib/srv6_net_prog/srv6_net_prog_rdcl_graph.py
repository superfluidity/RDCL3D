#
#   Copyright 2017 CNIT - Consorzio Nazionale Interuniversitario per le Telecomunicazioni
#
#   Licensed under the Apache License, Version 2.0 (the "License");
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
from lib.rdcl_graph import RdclGraph

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('Srv6_net_progRdclGraph')

class Srv6_net_progRdclGraph(RdclGraph):
    """Operates on the graph representation used for the GUI graph views"""

    def __init__(self):
        pass


    def build_graph_from_project(self, json_project, model={}):
        """Creates a single graph for a whole project"""

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


        except Exception as e:
            log.exception('Exception in build_graph_from_project')
            raise

        return graph_object

    def build_graph_from_descriptor(self, json_data, positions={}, model={}):
        """Creates a single graph from descriptor"""

        try:
            graph_object = json_data
            for node in graph_object['vertices']:
                if positions and 'vertices' in positions and node['id'] in positions['vertices'] and 'x' in positions['vertices'][node['id']] and 'y' in positions['vertices'][node['id']]:
                    node['fx'] = positions['vertices'][node['id']]['x']
                    node['fy'] = positions['vertices'][node['id']]['y']
            graph_object['model'] = model
        except Exception as e:
            log.exception('Exception in build_graph_from_project')
            raise

        return graph_object