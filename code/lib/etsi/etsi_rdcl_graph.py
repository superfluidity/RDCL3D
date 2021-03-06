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
log = logging.getLogger('EtsiRdclGraph')


class EtsiRdclGraph(RdclGraph):
    """Operates on the graph representation used for the GUI graph views"""

    def __init__(self):
        pass

    def create_vnf_views(self, vnfd, positions, graph_object):
        for vl in vnfd['intVirtualLinkDesc']:
            self.add_node(vl['virtualLinkDescId'], 'vnf_vl', vnfd['vnfdId'], positions, graph_object)
        for cpd in vnfd['vnfExtCpd']:
            self.add_node(cpd['cpdId'], 'vnf_ext_cp', vnfd['vnfdId'], positions, graph_object)
            self.add_link(cpd['cpdId'], cpd["intVirtualLinkDesc"], 'vnf', vnfd['vnfdId'], graph_object)
        for vdu in vnfd['vdu']:
            self.add_node(vdu['vduId'], 'vnf_vdu', vnfd['vnfdId'], positions, graph_object)
            for cpd in vdu['intCpd']:
                self.add_node(cpd['cpdId'], 'vnf_vdu_cp', vnfd['vnfdId'], positions, graph_object)
                self.add_link(cpd['cpdId'], cpd["intVirtualLinkDesc"], 'vnf', vnfd['vnfdId'], graph_object)
                self.add_link(cpd['cpdId'], vdu['vduId'], 'vnf', vnfd['vnfdId'], graph_object)

    def add_vnffgd_to_node(self, graph_object, node_id, vnffgdId):
        node = next((x for x in graph_object['vertices'] if x['id'] == node_id), None)
        if node is not None:
            node['info']['group'].append(vnffgdId)

    def add_vnffgd_to_links(self, graph_object, vnffgdId):
        for link in graph_object['edges']:
            source_node = next((x for x in graph_object['vertices'] if x['id'] == link['source']), None)
            target_node = next((x for x in graph_object['vertices'] if x['id'] == link['target']), None)
            # print "source node, target node :", source_node, target_node
            if vnffgdId in source_node['info']['group'] and vnffgdId in target_node['info']['group']:
                link['group'].append(vnffgdId)

    def build_graph_from_project(self, json_project, model={}):
        """Creates a single graph for a whole project"""

        # print "json_project ",json_project
        graph_object = {
            'vertices': [],
            'edges': [],
            'graph_parameters': {'vnffgIds': []},
            # 'model': Util().get_graph_model()
            'model': model
        }
        try:
            positions = json_project['positions'] if 'positions' in json_project else False
            log.debug('build t3d graph from project json')
            if 'vnfd' in json_project:
                for vnfd_id in json_project['vnfd']:
                    self.create_vnf_views(json_project['vnfd'][vnfd_id], positions, graph_object)
            if 'nsd' in json_project:
                for current_nsd in json_project['nsd']:
                    self.add_node(current_nsd, 'ns', current_nsd, positions, graph_object)
                    for vnfd_id in json_project['nsd'][current_nsd]['vnfdId']:
                        self.add_node(vnfd_id, 'vnf', current_nsd, positions, graph_object)
                    for sapd in json_project['nsd'][current_nsd]['sapd']:
                        self.add_node(sapd["cpdId"], 'ns_cp', current_nsd, positions, graph_object)
                        if 'nsVirtualLinkDescId' in sapd:
                            self.add_link(sapd['nsVirtualLinkDescId'], sapd["cpdId"], 'ns', current_nsd, graph_object)
                        elif 'associatedCpdId' in sapd:
                            associatedCpdId = next(
                                (x for x in graph_object['vertices'] if x['id'] == sapd['associatedCpdId']), None)
                            self.add_link(associatedCpdId['info']['group'], sapd["cpdId"], 'ns', current_nsd,
                                          graph_object)
                    for vld in json_project['nsd'][current_nsd]['virtualLinkDesc']:
                        self.add_node(vld["virtualLinkDescId"], 'ns_vl', current_nsd, positions, graph_object)
                    for nsdf in json_project['nsd'][current_nsd]['nsDf']:
                        for vnfProfile in nsdf['vnfProfile']:
                            for nsVirtualLinkConnectivity in vnfProfile["nsVirtualLinkConnectivity"]:
                                virtualLinkProfile = next((x for x in nsdf['virtualLinkProfile'] if
                                                           x['virtualLinkProfileId'] == nsVirtualLinkConnectivity[
                                                               'virtualLinkProfileId']), None)
                                if (virtualLinkProfile is not None):
                                    self.add_link(virtualLinkProfile['virtualLinkDescId'], vnfProfile["vnfdId"], 'ns',
                                                  current_nsd, graph_object)
                    for vnffgd in json_project['nsd'][current_nsd]['vnffgd']:
                        graph_object['graph_parameters']['vnffgIds'].append(vnffgd['vnffgdId'])
                        for vnfdId in vnffgd['vnfdId']:
                            self.add_vnffgd_to_node(graph_object, vnfdId, vnffgd['vnffgdId'])
                        for cpdPoolId in vnffgd['cpdPoolId']:
                            self.add_vnffgd_to_node(graph_object, cpdPoolId, vnffgd['vnffgdId'])
                        for virtualLinkDescId in vnffgd['virtualLinkDescId']:
                            self.add_vnffgd_to_node(graph_object, virtualLinkDescId, vnffgd['vnffgdId'])
                        self.add_vnffgd_to_links(graph_object, vnffgd['vnffgdId'])

        except Exception as e:
            log.error('Exception in build_graph_from_project')
            raise

        return graph_object
