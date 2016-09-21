import json
import pkgutil


class ciscoapic():
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

    def validate(self, topology):
        result = {}
        return result

    """docstring for ciscoapic"""

    def __init__(self, arg):
        # super(oshi, self).__init__()

        self.model_name = 'ciscoapic'

        self.list_of_all_node_types = ["Host", "Switch", "Router", "Cloud Node", "Wired Host", "Wireless Host"]

        self.list_of_all_layer = ["Data", "Control"]

        self.graph_parameters = {
            "tunneling": "OPENVPN",
            "testbed": "MININET",
            "mapped": "",
            "vlan": "",
            "generated": ""
        }

        self.nodes = {}

        self.nodes["Switch"] = {
            "node_label": 'switch',
            "properties": {
                "custom_label": "",
            }
        }

        self.nodes["Host"] = {
            "node_label": 'host',
            "properties": {
                "custom_label": "",
            }
        }

        self.nodes["Router"] = {
            "node_label": 'router',
            "properties": {
                "custom_label": "",
            }
        }

        self.nodes["Cloud Node"] = {
            "node_label": 'Cloud Node',
            "properties": {
                "custom_label": "",
            }
        }

        self.nodes["Wired Host"] = {
            "node_label": 'Wired Host',
            "properties": {
                "custom_label": "",
            }
        }

        self.nodes["Wireless Host"] = {
            "node_label": 'Wireless Host',
            "properties": {
                "custom_label": "",
            }
        }

        self.layer_constraints = {}

        self.layer_constraints["Data"] = {
            "multihoming": "false",
            "changing_nodes_type": True,
            "selectable_edges":[
                { "role" : ["Cloud Node", "Border Router"]}
            ],
            "edges-properties": {
                "bw": ""
            }
        }

        self.layer_constraints['Control'] = {
            "list_of_nodes_layer": [
                "Router",
                "Switch"
            ],
            "changing_nodes_type": "false",
            "insert_new_node": "false"

        }
