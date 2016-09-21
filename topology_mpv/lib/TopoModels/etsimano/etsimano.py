import json
import pkgutil
import re

class etsimano():

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

    #TODO
    def validate(self, topology):
        result = {}
        return result

    def __init__(self, arg):

        self.model_name = 'etsimano'
        #TODO
        self.list_of_all_node_types = ["vnf", "vnfc","vnf_cp", "vnfc_cp", "ns_cp", "ns_vl", "vnf_vl", "vdu"]

        #TODO
        self.list_of_all_layer = ["nsd", "vnfd"]

        self.graph_parameters = {}

        self.nodes = {}

        self.nodes["vnf"] = {
            "node_label": 'vnf',
            "properties": {
                "custom_labe": ""
            }
        }

        self.nodes["vnfc"] = {
            "node_label": 'vnfc',
            "properties": {
                "custom_labe": ""
            }
        }

        self.nodes["evl"] = {
            "node_label": 'vl',
            "properties": {
                "custom_labe": ""
            }
        }

        self.nodes["ivl"] = {
            "node_label": 'vl',
            "properties": {
                "custom_labe": ""
            }
        }

        self.layer_constraints = {}

        self.layer_constraints["nsd"] = {
            "list_of_nodes_layer": ["vnf", "ns_cp", "ns_vl"]
        }

        self.layer_constraints["vnfd"] = {
            "list_of_nodes_layer": ["vnfc", "vnf_vl", "vnf_cp", "vdu", "vnfc_cp"]
        }
