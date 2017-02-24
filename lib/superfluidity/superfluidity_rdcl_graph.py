import json
import logging
import copy

from lib.clickparser import click_parser
from lib.etsi.etsi_rdcl_graph import EtsiRdclGraph
from lib.rdcl_graph import RdclGraph

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('SuperfluidityRdclGraph')

class SuperfluidityRdclGraph(RdclGraph):
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
            etsi_topology = EtsiRdclGraph().build_graph_from_project(json_project)
            click_vertices = []
            click_edges = []
            click_topology = click_parser.importprojectjson(json_project, positions=positions)
            click_vertices = click_vertices  + click_topology['vertices']
            click_edges = click_edges + click_topology['edges']
            for vnf_id in json_project['vnfd']:
                vnfd = json_project['vnfd'][vnf_id]
                for vdu in vnfd['vdu']:
                    if 'vduNestedDescType' in vdu and vdu['vduNestedDescType'] == 'click' and vdu['vduNestedDesc'] and vdu['vduNestedDesc'] in json_project['click']:
                        vertice =  next((x for x in etsi_topology['vertices'] if x['id'] == vdu['vduId']), None)
                        if vertice is not None:
                            vertice['id'] = vdu['vduNestedDesc']
                            vertice['info']['type'] = 'vnf_click_vdu'
                            vertice['group'] = [vdu['vduNestedDesc']]
                            vertice['vduId'] = vdu['vduId']
                            if positions and vertice['id']  in positions['vertices']:
                                vertice['fx'] = positions['vertices'][vertice['id']]['x']
                                vertice['fy'] = positions['vertices'][vertice['id']]['y']
                        for edge in etsi_topology['edges']:
                            if edge['source'] == vdu['vduId']:
                                edge['source'] = vdu['vduNestedDesc']
                                edge['vduId'] = vdu['vduId']
                            if edge['target'] == vdu['vduId']:
                                edge['target'] = vdu['vduNestedDesc']
                                edge['vduId'] = vdu['vduId']

            graph_object['vertices'] = etsi_topology['vertices'] + click_vertices
            graph_object['edges'] = etsi_topology['edges'] + click_edges
            log.debug('build graph from project json')


        except Exception as e:
            log.exception('Exception in build_graph_from_project')
            raise

        return graph_object
