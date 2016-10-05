from django.http import HttpResponseRedirect
from django.shortcuts import render
from lib.emparser import emparser
from lib.emparser.t3d_util import T3DUtil
from lib.emparser.util import Util
from django.http import HttpResponse
import json
from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.template.loader import render_to_string


def base(request, configuration_id=None):
    test_t3d = T3DUtil()
    emautil = Util()
    #topology_baton = emautil.loadjsonfile('/Users/francesco/Workspace/sf_t3d/sf_dev/examples/nsd_oimsc_unique/nsd.json')
    project = emparser.importproject('/Users/francesco/Workspace/sf_t3d/sf_dev/examples/my_example/JSON', 'json')
    topology = test_t3d.build_graph_from_project(project)
    print type(topology)
    
    return render(request, 'basedev.html', {'configuration': '', 'topology_string': json.dumps(topology)})


def d3js(request, configuration_id=None):
    test_t3d = T3DUtil()
    emautil = Util()
    # topology_baton = emautil.loadjsonfile('/Users/francesco/Workspace/sf_t3d/sf_dev/examples/nsd_oimsc_unique/nsd.json')
    project = emparser.importproject('/Users/francesco/Workspace/sf_t3d/sf_dev/examples/my_example/JSON', 'json')
    topology = test_t3d.build_graph_from_project(project)
    print type(topology)

    return render(request, 'basedev_d3js.html', {'configuration': '', 'topology_string': json.dumps(topology)})




# Create your views here.
def topology_test(request, configuration_id=None):
    test_t3d = T3DUtil()
    project = emparser.importproject('/Users/francesco/Workspace/sf_t3d/sf_dev/examples/my_example/JSON', 'json')
    topology = test_t3d.build_graph_from_project(project)
    # print response
    response =  HttpResponse(json.dumps(topology), content_type="application/json")
    response["Access-Control-Allow-Origin"] = "*"
    return response


