from django.http import HttpResponseRedirect
from django.shortcuts import render
from lib.emparser import emparser
from lib.emparser.t3d_util import T3DUtil
from lib.emparser.util import Util
import json


def base(request, configuration_id=None):
    test_t3d = T3DUtil()
    emautil = Util()
    #topology_baton = emautil.loadjsonfile('/Users/francesco/Workspace/sf_t3d/sf_dev/examples/nsd_oimsc_unique/nsd.json')
    project = emparser.importproject('/Users/francesco/Workspace/sf_t3d/sf_dev/examples/my_example/JSON', 'json')
    topology = test_t3d.build_graph_from_project(project)
    print type(topology)
    
    return render(request, 'basedev.html', {'configuration': '', 'topology_string': json.dumps(topology)})
