import json
import logging
import copy
from util import Util


class T3DUtil:

    node_t3d_base = {
        'v':{
            'x': 0.1,
            'y': 0.1
        },
        'info': {
            'frozen': False,
            'property': {
                'custom_label': '',
                'role': ''
            },
            'type': ''
        }
    }

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        self.log = logging.getLogger('T3DUtil')

    def __build_nodes_ns(self, graph_object, project_data):
        self.log.debug('__build_nodes')
        for nscp in project_data['nsd']['connection_point']:
            id_nscp = 'id'
            graph_object['vertices'][nscp[id_nscp]] = self.__build_node_ns_cp(nscp)

        return graph_object

    def __build_node_ns_cp(self, cpdata):
        node = copy.deepcopy(self.node_t3d_base)

        node['cp_info'] = cpdata
        node['info']['type'] = 'ns_cp'
        node['info']['property']['role'] = 'circular'
        return node

    def __build_node_ns_vld(self, vldata):
        node = copy.deepcopy(self.node_t3d_base)
        node['info']['type'] = 'ns_vl'
        node['info']['property']['role'] = 'circular'
        node['vl_info'] = vldata
        return node



    def __build_edges_ns_vld(self, nsdid, vldid, json_project, graph_object):

        for vl_cp in json_project['vld'][vldid]['connection']:
            #cerco connessione con ns:connection_point
            for ns_cp in json_project['nsd'][nsdid]['connection_point']:
                if vl_cp == ns_cp['id']:
                    edge_identifier = vldid + '&&' + vl_cp
                    if edge_identifier not in graph_object['edges'].keys():
                        graph_object['edges'][edge_identifier] = {
                            'links': []
                        }
                    graph_object['edges'][edge_identifier]['links'].append({
                        'id': edge_identifier,
                        'view': 'nsd'
                    })

            # cerco connessione con vnfd livello ns
            for vnfd_id in json_project['vnfd']:
                for vnfd_cp in json_project['vnfd'][vnfd_id]['connection_point']:
                    if vl_cp == vnfd_cp['id']:
                        edge_identifier = vldid + '&&' + vnfd_id
                        if edge_identifier not in graph_object['edges'].keys():
                            graph_object['edges'][edge_identifier] = {
                                'links': []
                            }
                        graph_object['edges'][edge_identifier]['links'].append({
                            'id': vldid + '&&' + vl_cp,
                            'view': 'nsd'
                        })

        return graph_object

    def __parse_ns_vnfd(self, vnfdid, vnfd, graph_object):
        vnfd_node = copy.deepcopy(self.node_t3d_base)
        vnfd_node['info']['type'] = 'vnf'
        vnfd_node['info']['property']['role'] = 'circular'
        graph_object['vertices'][vnfdid] = vnfd_node
        for vnfd_cp in vnfd['connection_point']:
            vnfd_cp_node = copy.deepcopy(self.node_t3d_base)
            vnfd_cp_node['info']['type'] = 'vnf_cp'
            vnfd_cp_node['vnfd_cp_info'] = vnfd_cp
            graph_object['vertices'][vnfd_cp['id']] = vnfd_cp_node

        for vnfd_vl in vnfd['virtual_link']:
            vnfd_vl_node = copy.deepcopy(self.node_t3d_base)
            vnfd_vl_node['info']['type'] = 'vnf_vl'
            vnfd_vl_node['vnfd_vl_info'] = vnfd_vl
            graph_object['vertices'][vnfd_vl['id']] = vnfd_vl_node
            for vnfd_vl_cp_r in vnfd_vl['connection_points_references']:
                edge_identifier = vnfd_vl['id'] + '&&' + vnfd_vl_cp_r
                graph_object = self.__addLinktoEdge(edge_identifier, edge_identifier, 'vnfd', graph_object)


        for vdu in vnfd['vdu']:
            vdu_node = copy.deepcopy(self.node_t3d_base)
            vdu_node['info']['type'] = 'vdu'
            vdu_node['vdu_info'] = vdu
            graph_object['vertices'][vdu['id']] = vdu_node
            for vnfc in vdu['vnfc']:
                vnfc_node = copy.deepcopy(self.node_t3d_base)
                vnfc_node['info']['type'] = 'vnfc'
                vnfc_node['vnfc_info'] = vnfc
                graph_object['vertices'][vnfc['id']] = vnfc_node
                edge_identifier = vdu['id'] + "&&" + vnfc['id']
                graph_object = self.__addLinktoEdge(edge_identifier,edge_identifier,'vnfd', graph_object)
                for vnfc_cp in vnfc['connection_point']:
                    vnfc_cp_node = copy.deepcopy(self.node_t3d_base)
                    vnfc_cp_node['info']['type'] = 'vnfc_cp'
                    vnfc_node['vnfc_cp_info'] = vnfc_cp
                    graph_object['vertices'][vnfc_cp['id']] = vnfc_cp_node
                    edge_identifier = vnfc['id'] + '&&' + vnfc_cp['id']
                    graph_object = self.__addLinktoEdge(edge_identifier, edge_identifier, 'vnfd', graph_object)



        return graph_object

    def __addLinktoEdge(self, edge_identifier, link_identifier, view, graph_object):
        if edge_identifier not in graph_object['edges'].keys():
            graph_object['edges'][edge_identifier] = {
                'links': []
            }
        graph_object['edges'][edge_identifier]['links'].append({
            'id': link_identifier,
            'view': view
        })

        return graph_object

    def build_graph_from_project(self, json_project):
        graph_object = {
            'vertices': {},
            'edges': {},
            'graph_parameters': {}
        }
        try:
            self.log.debug('build t3d graph from project json')

            for current_nsd in json_project['nsd']:
                print current_nsd, json_project['nsd'][current_nsd]['connection_point']
                for nscp in json_project['nsd'][current_nsd]['connection_point']:
                    id_nscp = 'id'
                    graph_object['vertices'][nscp[id_nscp]] = self.__build_node_ns_cp(nscp)

                for vldid in json_project['nsd'][current_nsd]['vld']:
                    vld = json_project['vld'][vldid]
                    graph_object['vertices'][vldid] = self.__build_node_ns_vld(vld)
                    graph_object = self.__build_edges_ns_vld(current_nsd, vldid, json_project, graph_object)
                    # graph_object = self.__build_nodes_ns(graph_object, json_project)
                    # graph_object = self.__build_edges(graph_object, json_project)

                for vnfdid in json_project['nsd'][current_nsd]['vnfd']:
                    vnfd = json_project['vnfd'][vnfdid]
                    graph_object = self.__parse_ns_vnfd(vnfdid, vnfd, graph_object)

        except Exception as e:
            self.log.error('Exception build_graph_from_project')
            raise
        self.log.debug('\n' + json.dumps(graph_object))
        return graph_object
