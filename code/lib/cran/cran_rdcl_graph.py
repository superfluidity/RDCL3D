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

import logging
from lib.rdcl_graph import RdclGraph

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('CranRdclGraph')


class CranRdclGraph(RdclGraph):
    """Operates on the graph representation used for the GUI graph views"""

    def __init__(self):
        pass

    def build_graph_from_project(self, json_project, model={}):
        """Creates a single graph for a whole project"""

        graph_object = {
            'vertices': [],
            'edges': [],
            'graph_parameters': {},
            'model': model
        }
        try:
            log.debug('build graph from project json')

        except Exception as e:
            log.exception('Exception in build_graph_from_project')
            raise

        return graph_object

    def build_graph_from_descriptor(self, descriptor, positions, model={}):
        """Creates a single graph for a descriptor"""
        graph_object = {
            'vertices': [],
            'edges': [],
            'graph_parameters': {},
            'model': model
        }

        try:
            log.debug('build graph from descriptor json')
            functional_blocks = descriptor['Functional-blocks']
            for f_block in functional_blocks:
                type_fb = f_block['type'] if 'type' in f_block else 'functional_block'
                self.add_node(f_block['name'], type_fb, False, positions, graph_object)
                if 'rfb-list' in f_block:
                    for rfb in f_block['rfb-list']:
                        rfb_data = self.get_functional_block(rfb, functional_blocks)
                        target_type = rfb_data['type'] if 'type' in rfb_data else 'functional_block'

                        directed = self.is_directed_edge(source_type=type_fb, target_type=target_type, layer='full',
                                                         model=model)
                        optional = {
                            'type_link': 'hierarchical',
                            'directed_edge': directed
                        }
                        self.add_link(f_block['name'], rfb, 'full', None, graph_object, optional=optional)
                if 'links' in f_block:
                    for link in f_block['links']:
                        rfb_data = self.get_functional_block(link, functional_blocks)
                        target_type = rfb_data['type'] if 'type' in rfb_data else 'functional_block'

                        directed_full = self.is_directed_edge(source_type=type_fb, target_type=target_type,
                                                              layer='full', model=model)
                        optional = {
                            'type_link': 'same_level',
                            'directed_edge': directed_full
                        }
                        self.add_link(f_block['name'], link, 'full', None, graph_object,optional=optional)
                        directed_level_c = self.is_directed_edge(source_type=type_fb, target_type=target_type,
                                                                 layer=f_block['rfb-level'], model=model)
                        optional = {
                            'type_link': 'same_level',
                            'directed_edge': directed_level_c
                        }
                        self.add_link(f_block['name'], link, f_block['rfb-level'], None, graph_object, optional=optional)

        except Exception as e:
            log.exception('Exception in build_graph_from_descriptor')
            raise
        return graph_object

    def get_functional_block(self, name, fb_list):
        for fb in fb_list:
            if fb['name'] == name:
                return fb
