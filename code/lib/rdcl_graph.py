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

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('RdclGraph')


class RdclGraph(object):
    """ Operates on the graph representation used for the GUI graph views """

    node_t3d_base = {
        'info': {
            'property': {
                'custom_label': '',
            },
            'type': '',
            'group': []
        }
    }

    def __init__(self):
        pass

    def add_link(self, source, target, view, group, graph_object ):
        if (source is None) or (target is None):
            return;
        edge_obj = {
            'source': source,
            'target': target,
            'view': view,
            'group': [group]
        }
        if edge_obj not in graph_object['edges']:
            graph_object['edges'].append(edge_obj)

    def add_node(self, id, type, group, positions, graph_object):
        if id is None:
            return
        node = next((x for x in graph_object['vertices'] if x['id'] == id), None)
        if node is not None:
            node['info']['group'].append(group)
        else:
            node = copy.deepcopy(self.node_t3d_base)
            node['id'] = id
            node['info']['type'] = type
            node['info']['group'].append(group)
            if positions and id in positions['vertices'] and 'x' in positions['vertices'][id] and 'y' in positions['vertices'][id] :
                node['fx'] = positions['vertices'][id]['x']
                node['fy'] = positions['vertices'][id]['y']
            graph_object['vertices'].append(node)

