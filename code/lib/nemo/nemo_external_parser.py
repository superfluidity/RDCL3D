class Nemo_Intent:

    sentences = []
    objects = []
    operations = []

    def __init__(self, intent_text):
        self.objects = Nemo_objects()
        #Get sentences
        sentences = intent_text.split('\n')
        while '' in sentences:
            sentences.remove('')
        self.sentences = sentences

        #Go over the intent sentence by sentence
        for sentence in self.sentences:
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
                           
                    self.objects.append_Node(name, node_type, subnodes, properties)  

                #Get connections
                if words[1] == 'Connection':
                       name = words[2]
                       index = 4
                       endpoints = []
                       while index < len(words):
                           endpoints.append(words[index])    
                           index = index + 1
                       self.objects.append_Connect(name, endpoints)

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
            objects_dict['nodes'].append(node.to_dict())
        for flow in self.flows:
            objects_dict['flows'].append(str(flows))
        for conn in self.connections:
            objects_dict['connections'].append(conn.to_dict())
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

    def to_dict(self):
        node_dict = { "name": self.name, "type":  self.node_type}
        if self.properties:
            node_dict["properties"] = self.properties
        if self.sub_nodes:
            node_dict["subnodes"] = self.sub_nodes
        return node_dict

class Nemo_Connection:

    name = None
    endpoints = []

    def __init__(self, name, endpoints):
        self.name = name
        self.endpoints = endpoints

    def __str__(self):
        string = "name: " + self.name + '\n' + "endpoints: " + str(self.endpoints)
        return string

    def to_dict(self):
        conn_dict = {"name": self.name, "endpoints": self.endpoints}
        return conn_dict
        

class Nemo_Nodemodel:

    name = None
    sub_nodes = []
    properties = []

    def __init__(self, node_text):
        node_text = node_text.replace('\n', '')
        node_text = node_text.replace(',','')
        node_text = node_text.replace(';','')
        words = node_text.split(' ')
        self.name = words[2]
        if len(words) > 3:
            index = 4
            if words[3] == 'Property':
                while index < len(words) - 1:
                    properties.append(words[index + 1])
                    index = index + 2
                self.properties = properties
            if words[3] == 'Contain':
                while index < len(words):
                    subnodes.append(words[index])
                    index = index + 1
                self.subnodes = subnodes

    def __str__(self):
        string = "name: " + self.name + '\n'
        if self.properties:
            string = string +'\n' + "properties: " + str(self.properties)
        if self.sub_nodes:
            string = string + '\n' + "subnodes: " + str(self.sub_nodes)
        return string

    def to_dict(self):
        node_dict = { "name": self.name}
        if self.properties:
            node_dict["properties"] = self.properties
        if self.sub_nodes:
            node_dict["subnodes"] = self.sub_nodes
        return node_dict

