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
            },
            'type': ''
        }
    }

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        self.log = logging.getLogger('T3DUtil')

    def add_link(self, source, target, view, group, graph_object ):
        if (source is None) or (target is None):
            return;
        edge_obj = {
            'source': source,
            'target': target,
            'view': view,
            'group': group
        }
        if edge_obj not in graph_object['edges']:
            graph_object['edges'].append(edge_obj)

    def add_node(self, id, type, group, positions, graph_object):
        node = copy.deepcopy(self.node_t3d_base)
        node['id'] = id
        node['info']['type'] = type
        node['info']['group'] = group
        if positions and id in positions['vertices'] and 'x' in positions['vertices'][id] and 'y' in positions['vertices'][id] :
            node['fx'] = positions['vertices'][id]['x']
            node['fy'] = positions['vertices'][id]['y']
        graph_object['vertices'].append(node)

    def create_vnf_views(self, vnfd, positions, graph_object):
        for vl in vnfd['intVirtualLinkDesc']:
            self.add_node(vl['virtualLinkDescId'], 'vnf_vl', vnfd['vnfdId'],positions, graph_object)
        for cpd in vnfd['vnfExtCpd']:
            self.add_node(cpd['cpdId'], 'vnf_ext_cp', vnfd['vnfdId'], positions, graph_object)
            self.add_link(cpd['cpdId'], cpd["intVirtualLinkDesc"], 'vnf', vnfd['vnfdId'], graph_object)
        for vdu in vnfd['vdu']:
            self.add_node(vdu['vduId'], 'vnf_vdu', vnfd['vnfdId'], positions, graph_object)
            for cpd in vdu['intCpd']:
                self.add_node(cpd['cpdId'], 'vnf_vdu_cp', vnfd['vnfdId'], positions, graph_object)
                self.add_link(cpd['cpdId'], cpd["intVirtualLinkDesc"], 'vnf', vnfd['vnfdId'], graph_object)
                self.add_link(cpd['cpdId'], vdu['vduId'], 'vnf', vnfd['vnfdId'], graph_object)

    def build_graph_from_project(self, json_project):
        print "json_project ",json_project
        graph_object = {
            'vertices': [],
            'edges': [],
            'graph_parameters': {}
        }
        try:
            positions = json_project['positions'] if 'positions' in json_project else False
            self.log.debug('build t3d graph from project json')

            for vnfd_id in json_project['vnfd']:
                self.create_vnf_views(json_project['vnfd'][vnfd_id], positions, graph_object)
            for current_nsd in json_project['nsd']:
                self.add_node(current_nsd, 'ns', current_nsd, positions, graph_object)
                for vnfd_id in json_project['nsd'][current_nsd]['vnfdId']:
                    self.add_node(vnfd_id, 'vnf', current_nsd, positions, graph_object)
                for sapd in json_project['nsd'][current_nsd]['sapd']:
                    self.add_node(sapd["cpdId"], 'ns_cp', current_nsd, positions, graph_object)
                    self.add_link(sapd['nsVirtualLinkDescId'], sapd["cpdId"], 'ns', current_nsd, graph_object)
                for vld in json_project['nsd'][current_nsd]['virtualLinkDesc']:
                   self.add_node(vld["virtualLinkDescId"], 'ns_vl', current_nsd, positions, graph_object)
                for nsdf in json_project['nsd'][current_nsd]['nsDf']:
                    for vnfProfile in nsdf['vnfProfile']:
                        for nsVirtualLinkConnectivity in vnfProfile["nsVirtualLinkConnectivity"]:
                            virtualLinkProfile = next((x for x in nsdf['virtualLinkProfile'] if x['virtualLinkProfileId'] == nsVirtualLinkConnectivity['virtualLinkProfileId']), None)
                            if(virtualLinkProfile is not None):
                                self.add_link(virtualLinkProfile['virtualLinkDescId'], vnfProfile["vnfdId"], 'ns', current_nsd, graph_object)

        except Exception as e:
            self.log.error('Exception build_graph_from_project')
            raise
        self.log.debug('Graph\n' + json.dumps(graph_object))
        return graph_object
