class Nemo_Intent:

    sentences = []
    objects = []
    operations = []

    def __init__(self):
        self.objects = Nemo_objects()

    def to_dict(self):
        intent_dict=self.objects.to_dict()
        return intent_dict

class Nemo_objects:

    nodes = []
    flows = []
    connections = []

    def append_Node(self, name, node_type, subnodes=None, properties=None):
        self.nodes.append(Nemo_Node(name, node_type, subnodes, properties))

    def append_Connect(self, name, endpoints):
        self.connections.append(Nemo_Connection(name, endpoints))

    def to_dict(self):
        objects_dict = {'nodes': [], 'flows': [], 'connections': []}
        for node in self.nodes:
            objects_dict['nodes'].append(str(node))
        for flow in self.flows:
            objects_dict['flows'].append(str(flows))
        for conn in self.connections:
            objects_dict['connections'].append(str(conn))
        return objects_dict

class Nemo_Node:

    name = None
    node_type = None
    sub_nodes = []
    properties = []

    def __init__(self, name, node_type, subnodes=None, properties=None):
        self.name = name
        self.node_type = node_type
        if subnodes:
            self.sub_nodes = subnodes
        if properties:
            self.properties = properties

    def __str__(self):
        string = "name: " + self.name + '\n' + "type: " + self.node_type
        if self.properties:
            string = string +'\n' + "properties: " + str(self.properties)
        if self.sub_nodes:
            string = string + '\n' + "subnodes: " + str(self.sub_nodes)
        return string

class Nemo_Connection:

    name = None
    endpoints = []

    def __init__(self, name, endpoints):
        self.name = name
        self.endpoints = endpoints

    def __str__(self):
        string = "name: " + self.name + '\n' + "endpoints: " + str(self.endpoints)
        return string

def parse_Intent(intent_text):
    Intent = Nemo_Intent()

    #Read intent file
    #f = open(intent_file, 'r')
    #intent_text = f.read()

    #Get sentences
    sentences = intent_text.split('\n')
    while '' in sentences:
        sentences.remove('')
    Intent.sentences = sentences

    #Go over the intent sentence by sentence
    for sentence in Intent.sentences:
        sentence = sentence.replace(',','')
        sentence = sentence.replace(';','')
        words = sentence.split(' ')
        if words[0] == 'CREATE' or words[0] == 'IMPORT':
            #Get nodes
            if words[1] == 'Node':
                name = words [2]
                node_type = words[4]
                properties = {}
                subnodes = []
                if len(words) > 5:
                    index = 6
                    if words[5] == 'Property':
                        while index < len(words) - 1:
                            node_property = words[index].replace(':', '')
                            properties[node_property] = words[index +1].replace('"', '')
                            index = index + 2
                    if words[5] == 'Contain':
                        while index < len(words):
                            subnodes.append(words[index])
                            index = index + 1
                           
                Intent.objects.append_Node(name, node_type, subnodes, properties)  

            #Get connections
            if words[1] == 'Connection':
                   name = words[2]
                   index = 4
                   endpoints = []
                   while index < len(words):
                       endpoints.append(words[index])
                       index = index + 1
                   Intent.objects.append_Connect(name, endpoints)

    return Intent
