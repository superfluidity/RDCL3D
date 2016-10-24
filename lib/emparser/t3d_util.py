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

    def __build_node_ns_cp(self, cpdata, nsd):
        node = copy.deepcopy(self.node_t3d_base)
        node['id'] = cpdata['id']
        node['descriptor'] = cpdata
        node['nsd'] = nsd
        node['info']['type'] = 'ns_cp'
        node['info']['property']['role'] = 'circular'
        return node

    def __build_node_ns_vld(self, vldata, nsd):
        node = copy.deepcopy(self.node_t3d_base)
        node['id'] = vldata['id']
        node['nsd'] = nsd
        node['descriptor'] = vldata
        node['info']['type'] = 'ns_vl'
        node['info']['property']['role'] = 'circular'
        node['vl_info'] = vldata
        return node



    def __build_edges_ns_vld(self, nsdid, vldid, json_project, graph_object, nsd):

        for vl_cp in json_project['vld'][vldid]['connection']:
            #cerco connessione con ns:connection_point
            for ns_cp in json_project['nsd'][nsdid]['connection_point']:
                if vl_cp == ns_cp['id']:
                    edge_obj = {
                        'source': vldid,
                        'target': vl_cp,
                        'view': 'nsd',
                        'nsd' : nsd
                    }
                    if edge_obj not in graph_object['edges']:
                        graph_object['edges'].append(edge_obj)

            # cerco connessione con vnfd livello ns
            for vnfd_id in json_project['vnfd']:
                for vnfd_cp in json_project['vnfd'][vnfd_id]['connection_point']:
                    if vl_cp == vnfd_cp['id']:
                        edge_identifier = vldid + '&&' + vnfd_id
                        edge_obj = {
                            'source': vldid,
                            'target': vnfd_id,
                            'view': 'nsd',
                            'nsd': nsd
                        }
                        if edge_obj not in graph_object['edges']:
                            graph_object['edges'].append(edge_obj)

        return graph_object

    def __parse_ns_vnfd(self, vnfdid, vnfd, graph_object, nsd):
        vnfd_node = copy.deepcopy(self.node_t3d_base)
        vnfd_node['info']['type'] = 'vnf'
        vnfd_node['info']['property']['role'] = 'circular'
        vnfd_node['id'] = vnfdid
        vnfd_node['nsd'] = nsd
        vnfd_node['descriptor'] = vnfd
        graph_object['vertices'].append(vnfd_node)
        for vnfd_cp in vnfd['connection_point']:
            vnfd_cp_node = copy.deepcopy(self.node_t3d_base)
            vnfd_cp_node['info']['type'] = 'vnf_cp'
            vnfd_cp_node['vnfd_cp_info'] = vnfd_cp
            vnfd_cp_node['id'] = vnfd_cp['id']
            vnfd_cp_node['nsd'] = nsd
            vnfd_cp_node['descriptor'] = vnfd_cp
            graph_object['vertices'].append(vnfd_cp_node)

        for vnfd_vl in vnfd['virtual_link']:
            vnfd_vl_node = copy.deepcopy(self.node_t3d_base)
            vnfd_vl_node['info']['type'] = 'vnf_vl'
            vnfd_vl_node['vnfd_vl_info'] = vnfd_vl
            vnfd_vl_node['id'] = vnfd_vl['id']
            vnfd_vl_node['nsd'] = nsd
            vnfd_vl_node['descriptor'] = vnfd_vl
            graph_object['vertices'].append( vnfd_vl_node)
            for vnfd_vl_cp_r in vnfd_vl['connection_points_references']:
                edge_obj = {
                    'source': vnfd_vl['id'],
                    'target': vnfd_vl_cp_r,
                    'nsd': nsd
                }
                graph_object = self.__addLinktoEdge(edge_obj, edge_obj, 'vnfd', graph_object)


        for vdu in vnfd['vdu']:
            vdu_node = copy.deepcopy(self.node_t3d_base)
            vdu_node['info']['type'] = 'vdu'
            vdu_node['vdu_info'] = vdu
            vdu_node['id'] = vdu['id']
            vdu_node['nsd'] = nsd
            vdu_node['descriptor'] = vdu
            graph_object['vertices'].append(vdu_node)
            for vnfc in vdu['vnfc']:
                vnfc_node = copy.deepcopy(self.node_t3d_base)
                vnfc_node['info']['type'] = 'vnfc'
                vnfc_node['vnfc_info'] = vnfc
                vnfc_node['id'] = vnfc['id']
                vnfc_node['nsd'] = nsd
                vnfc_node['descriptor'] = vnfc
                graph_object['vertices'].append(vnfc_node)
                edge_obj = {
                    'source': vdu['id'],
                    'target': vnfc['id'],
                    'nsd': nsd
                }
                graph_object = self.__addLinktoEdge(edge_obj,edge_obj,'vnfd', graph_object)
                for vnfc_cp in vnfc['connection_point']:
                    vnfc_cp_node = copy.deepcopy(self.node_t3d_base)
                    vnfc_cp_node['info']['type'] = 'vnfc_cp'
                    vnfc_node['vnfc_cp_info'] = vnfc_cp
                    vnfc_cp_node['id'] = vnfc_cp['id']
                    vnfc_cp_node['nsd'] = nsd
                    vnfc_cp_node['descriptor'] = vnfc_cp
                    graph_object['vertices'].append(vnfc_cp_node)
                    edge_obj = {
                        'source': vnfc['id'],
                        'target': vnfc_cp['id'],
                        'nsd': nsd
                    }
                    graph_object = self.__addLinktoEdge(edge_obj, edge_obj, 'vnfd', graph_object)



        return graph_object

    def __addLinktoEdge(self, edge_obj, link_identifier, view, graph_object):
        edge_obj['view'] = view
        if edge_obj not in graph_object['edges']:
            graph_object['edges'].append(edge_obj)


        return graph_object

    def build_graph_from_project(self, json_project):
        print "json_project ",json_project
        graph_object = {
            'vertices': [],
            'edges': [],
            'graph_parameters': {}
        }
        try:
            self.log.debug('build t3d graph from project json')

            for current_nsd in json_project['nsd']:
                node = copy.deepcopy(self.node_t3d_base)
                node['id'] = current_nsd
                node['descriptor'] = json_project['nsd'][current_nsd]
                node['info']['type'] = 'ns'
                node['info']['property']['role'] = 'square'
                graph_object['vertices'].append(node)
                for vnfd_id in json_project['nsd'][current_nsd]['vnfdId']:
                    node = copy.deepcopy(self.node_t3d_base)
                    node['id'] = vnfd_id
                    node['descriptor'] = json_project['vnfd'][vnfd_id]
                    node['info']['type'] = 'vnf'
                    node['info']['property']['role'] = 'circle'
                    graph_object['vertices'].append(node)

                for sapd in json_project['nsd'][current_nsd]['sapd']:
                    node = copy.deepcopy(self.node_t3d_base)
                    node['id'] = sapd["cpdId"]
                    node['descriptor'] = sapd
                    node['info']['type'] = 'ns_cp'
                    node['info']['property']['role'] = 'circle'
                    graph_object['vertices'].append(node)
                    edge_obj = {
                        'source': sapd['nsVirtualLinkDescId'],
                        'target': sapd["cpdId"],
                        'view': 'nsd',
                        'nsd': current_nsd
                    }
                    if edge_obj not in graph_object['edges']:
                        graph_object['edges'].append(edge_obj)
                for vld in json_project['nsd'][current_nsd]['virtualLinkDesc']:
                    node = copy.deepcopy(self.node_t3d_base)
                    node['id'] = vld["virtualLinkDescId"]
                    node['descriptor'] = vld
                    node['info']['type'] = 'ns_vl'
                    node['info']['property']['role'] = 'circle'
                    graph_object['vertices'].append(node)
                for nsdf in json_project['nsd'][current_nsd]['nsDf']:
                    for vnfProfile in nsdf['vnfProfile']:
                        vnfId=  vnfProfile["vnfdId"]
                        print vnfId
                        for nsVirtualLinkConnectivity in vnfProfile["nsVirtualLinkConnectivity"]:
                            virtualLinkProfile =  next((x for x in nsdf['virtualLinkProfile'] if x['virtualLinkProfileId'] == nsVirtualLinkConnectivity['virtualLinkProfileId']), None)
                            vldid = virtualLinkProfile['virtualLinkDescId']
                            edge_obj = {
                                'source': vldid,
                                'target': vnfId,
                                'view': 'nsd',
                                'nsd': current_nsd
                            }
                            if edge_obj not in graph_object['edges']:
                                graph_object['edges'].append(edge_obj)
        except Exception as e:
            self.log.error('Exception build_graph_from_project')
            raise
        self.log.debug('\n' + json.dumps(graph_object))
        return graph_object
