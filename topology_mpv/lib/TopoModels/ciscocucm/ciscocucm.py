import json
import pkgutil


class ciscocucm():
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

    def validate(self, topology):
        result = {}
        return result

    """docstring for ciscocucm"""

    def __init__(self, arg):
        # super(oshi, self).__init__()

        self.model_name = 'ciscocucm'

        self.list_of_all_node_types = ["location"]

        self.list_of_all_layer = ["Data", "Control"]

        self.graph_parameters = {
            "tunneling": "OPENVPN",
            "testbed": "MININET",
            "mapped": "",
            "vlan": "",
            "generated": ""
        }

        self.nodes = {}

        self.nodes["location"] = {
            "node_label": 'location',
            "properties": {
                "custom_label": "",
                "role": "",
                "node_id": ""
            }
        }



        self.layer_constraints = {}

        self.layer_constraints["Data"] = {
            "multihoming": "false",
            "changing_nodes_type": True,
            "not_allowed_edge": [
                {"source": "location", "not_allowed_des": []}
            ],
        }

        self.layer_constraints['Control'] = {
            "list_of_nodes_layer": [
                "location",

            ],
            "changing_nodes_type": "false",
            "insert_new_node": "false"

        }
