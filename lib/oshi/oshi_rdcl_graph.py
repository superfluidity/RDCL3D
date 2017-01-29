import json
import logging
import copy
from lib.rdcl_graph import RdclGraph

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('OshiRdclGraph')

class OshiRdclGraph(RdclGraph):
    """Operates on the graph representation used for the GUI graph views"""

    def __init__(self):
        pass


    def build_graph_from_project(self, json_project, model={}):
        """Creates a single graph for a whole project"""
        # in oshi is not supported
        graph_object = {
            'vertices': [],
            'edges': [],
            'graph_parameters': {},
            'model': model
        }
        # try:
        #
        #
        # except Exception as e:
        #     log.exception('Exception in build_graph_from_project')
        #     raise

        return graph_object

    def build_graph_from_oshi_descriptor(self, json_data, model={}):
        """Creates a single graph for a oshi descriptor"""

        try:
            graph_object = json_data
            graph_object['model'] = model

        except Exception as e:
            log.exception('Exception in build_graph_from_project')
            raise

        return graph_object