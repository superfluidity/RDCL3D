import json
import logging
import copy
from lib.rdcl_graph import RdclGraph
from lib.nemo.nemo_external_parser import Nemo_Intent, Nemo_Nodemodel

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('NemoRdclGraph')

class NemoRdclGraph(RdclGraph):
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
            log.debug('build graph from project json')

            if 'intent' in json_project:
                #intents = {}
                for intent in json_project['intent']:
                    #print "intent name", intent
                    #print "intent_conent ", json_project['intent'][intent]
                    self.create_views_for_intent(Nemo_Intent(json_project['intent'][intent]).to_dict(), intent, positions, graph_object)


            if 'nodemodel' in json_project:
                #nodemodels = {}
                for nodemodel in json_project['nodemodel']:
                    self.create_views_for_nodemodel(Nemo_Nodemodel(json_project['nodemodel'][nodemodel]).to_dict(), nodemodel, positions, graph_object)

            #print "intents ", intents
            #print "nodemodels ", nodemodels


        except Exception as e:
            log.exception('Exception in build_graph_from_project')
            raise

        #print "graph_object ", graph_object
        return graph_object

    def create_views_for_intent(self, intent, name, positions, graph_object):
        self.add_node(name, 'intent', name, positions, graph_object)
        for node in intent['nodes']:
            #print "node ", node
            self.add_node(node["name"], 'nodemodel', name, positions, graph_object)
        #print "links ", intent['connections']
        for link in intent['connections']:
            #print "link ", link
            self.add_link(link['endpoints'][0], link['endpoints'][1], 'intent', name, graph_object)

    def create_views_for_nodemodel(self, nodemodel, name, positions, graph_object):
        self.add_node(name, 'nodemodel', name, positions, graph_object)
        #print "nodemodel ", nodemodel
        for node in nodemodel['subnodes']:
            self.add_node(node, 'subnode', name, positions, graph_object)

        for nemo_property in nodemodel['properties']:
            #print "property ", nemo_property
            self.add_node(nemo_property, 'nemo_property', name, positions, graph_object)
            #print "node ", graph_object['vertices'][-1]
