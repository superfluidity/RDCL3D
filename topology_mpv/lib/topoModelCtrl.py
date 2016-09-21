import pkgutil
import sys
import os
import imp
import json
import re


# from TopoModels.oshi.oshi import oshi


class ModelController():
    def jsonmodel(self, modelname):

        try:  # gestire meglio la definizione del path del modello
            x = __import__('topology_mpv.lib.TopoModels.' + modelname + '.' + modelname, fromlist=[modelname])
        except ImportError, e:
            print "import error! %s" % e
            return json.dumps({'error': {'message': 'Model Spec not found'}})
        try:
            cls = getattr(x, modelname)
        except AttributeError, e:
            print "AttributeError!"
            return json.dumps({'error': {'message': 'Model Spec not found'}})
        self.a = cls('')
        # if(modelname == 'oshi'):
        #	a = oshi('')
        # else:
        #	return {}

        return self.a.to_JSON()

    """docstring for ModelController"""

    def __init__(self, arg):
        # super(ModelController, self).__init__()
        print ("ModelController_init", arg)
        self.arg = arg

    def validateTopology(self, topology, modelname):
        result = {}

        model = json.loads(self.jsonmodel(modelname))
        # print (model)
        ###validazione nodi
        jsontopology = json.loads(topology)
        # print jsontopology
        resvnodes = self.validateNodes(jsontopology['vertices'], model);

        if (resvnodes.has_key('error')):
            result.update(resvnodes)
        print "nodes validation end"

        resvedges = self.validateEgdes(jsontopology, model);
        print "edges validation end"
        print resvedges
        if (resvedges.has_key('error')):
            if (result.has_key('error')):
                result['error']['messages'] = result['error']['messages'] + resvedges['error']['messages']
            else:
                result.update(resvedges)
        resmodel = self.a.validate(jsontopology)
        if (resmodel.has_key('error')):
            if (result.has_key('error')):
                result['error']['messages'] = result['error']['messages'] + resmodel['error']['messages']
            else:
                result.update(resmodel)

        return result

    def validateNodes(self, nodes, model):
        result = {}
        messages = []
        # print model['list_of_all_node_types']
        for n in nodes.keys():
            try:
                if (not nodes[n]['info'].get('type', "") in model['list_of_all_node_types']):
                    messages.append({'Node-' + n: 'Node type not recognized by the model.'})
                pass
            except KeyError, e:
                # raise e
                # print e
                messages.append({'Node-' + n: 'Node properties not found.'})

        print messages

        if (len(messages) > 0):
            result = {'error': {'messages': messages}}
        return result

    def validateEgdes(self, topology, model):
        result = {}
        messages = []
        nodes = topology['vertices']
        edges = topology['edges']

        for e in edges.keys():
            enodes = e.split('&&')
            nodef = enodes[0]
            nodet = enodes[1]
            try:
                typef = nodes[nodef]['info']['type']
                typet = nodes[nodet]['info']['type']

                linkscounter = {}
                for l in edges[e]['links']:
                    # print "@@@ "
                    # print l
                    ##check node type not allowed
                    if (model['layer_constraints'][l['view']].has_key('list_of_nodes_layer') and len(
                            model['layer_constraints'][l['view']]['list_of_nodes_layer'])):
                        if (typef not in model['layer_constraints'][l['view']]['list_of_nodes_layer']):
                            messages.append({'Edge-' + e: 'Node ' + nodef + ' type ' + typef + ' not allowed.'})
                        if (typet not in model['layer_constraints'][l['view']]['list_of_nodes_layer']):
                            messages.append({'Edge-' + e: 'Node ' + nodet + ' type ' + typet + ' not allowed.'})

                    ##check not allowed edge
                    if (model['layer_constraints'][l['view']].has_key('not_allowed_edge')):
                        for n in model['layer_constraints'][l['view']]['not_allowed_edge']:
                            print typef, typet, n['source'], n['not_allowed_des']
                            if (n['source'] == typef and typet in n['not_allowed_des']):
                                messages.append({'Edge-' + e: 'Edge not allowed.'})
                    if (not linkscounter.has_key(l['view'])):
                        linkscounter[l['view']] = 0
                    linkscounter[l['view']] += 1
                pass
                print linkscounter
                for t in linkscounter.keys():
                    print model['layer_constraints'][t]
                    if (model['layer_constraints'][t].has_key('multilink') and model['layer_constraints'][t][
                        'multilink'] == 'false' and linkscounter[t] > 1):
                        messages.append({'Edge-' + e: 'Multilink in ' + t + ' not allowed.'})
            except KeyError, error:
                print "error male male", error
                messages.append({'Edge-' + e: 'Egde properties ' + str(error) + ' not found.'})
            # print nodef, nodet

        if (len(messages) > 0):
            result = {'error': {'messages': messages}}
        return result


if __name__ == '__main__':
    test = ModelController('ciao')
    print test.jsonmodel('oshi')
