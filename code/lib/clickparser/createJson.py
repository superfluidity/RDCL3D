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

VERTEX_INFO_KEY = 'info'

VERTEX_ID_KEY = 'id'

LINK_ID_KEY = 'id'

LINK_TYPE_KEY = 'depth'

LINK_GROUP = 'group'

NODE_TYPE_KEY = 'type'


def nx_2_t3d_json(element, connection, json_out_file):
    nodes_list = []

    for i in range(0, len(element)):
        nodes_dict = {}

        nodes_dict[VERTEX_INFO_KEY] = {}
        nodes_dict[VERTEX_INFO_KEY]['frozen'] = False
        nodes_dict[VERTEX_INFO_KEY][NODE_TYPE_KEY] = element[i]['node_type']
        nodes_dict[VERTEX_INFO_KEY]['property']={}
        nodes_dict[VERTEX_INFO_KEY]['property']['attributes'] = element[i]['config']
        nodes_dict[VERTEX_INFO_KEY]['property']['type_element'] = element[i]['element']
        nodes_dict[VERTEX_INFO_KEY]['group'] = element[i]['group']
        nodes_dict[VERTEX_ID_KEY] = element[i]['name']

        nodes_list.append(nodes_dict)

    edge_list = []

    for i in range(0, len(connection)):
        edge_dict = {}
        edge_dict['source'] = connection[i]['source']
        edge_dict[LINK_GROUP] = connection[i]['group']
        #edge_dict['group'].append('click')
        edge_dict['target'] = connection[i]['target']
        edge_dict[LINK_TYPE_KEY] = connection[i]['depth']
        edge_dict['view'] = connection[i]['view']

        edge_list.append(edge_dict)

    topo_dict = dict([('edges', edge_list), ('vertices', nodes_list)])

    json_data = json.dumps(topo_dict, sort_keys=True, indent=4)

    '''
    out_file = open(json_out_file,"w")
    out_file.write(str(json_data)+"\n")
    out_file.close()
    '''

    return json_data
