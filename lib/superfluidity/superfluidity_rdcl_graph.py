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
            graph_object['vertices'] = etsi_topology['vertices'] + click_vertices
            graph_object['edges'] = etsi_topology['edges'] + click_edges
            log.debug('build graph from project json')


        except Exception as e:
            log.exception('Exception in build_graph_from_project')
            raise

        return graph_object
