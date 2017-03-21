#
#   Copyright 2017 CNIT - Consorzio Nazionale Interuniversitario per le Telecomunicazioni
#
#   Licensed under the Apache License, Version 2.0 (the );
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an  BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from lib.oshi.oshi_parser import OshiParser
import json

@login_required
def user_deployments(request):
    #user = CustomUser.objects.get(id=request.user.id)
    deployments = [{
        'id': 1,
        'name': "OshiExp",
        'profile': "",
        'project_name': "OshiPrj",
        'project_id': 1,
        'creator_name': "admin",
        'creator_id': 1,
        'created_date': "2017-03-14 16:18",
        'status': "ready",
    }] #Deployment.objects.filter(owner=user).select_subclasses()
    result = {}
    result.update({'deployments': list(deployments)})
    return render(request, 'deployments_list.html', result)

@login_required
def open_deployment(request, deployment_id=None):
    try:

        deployment = {
            'id': 1,
            'name': "OshiExp",
            'profile': "",
            'project_name': "OshiPrj",
            'project_id': 1,
            'creator_name': "admin",
            'creator_id': 1,
            'created_date': "2017-03-14 16:18",
            'last_access_date': "2017-03-14 16:18",
            'status': "ready",
        }

        topology_data = OshiParser.importprojectdir('usecases/OSHI/example1', 'json')

        topology = topology_data['oshi']['example1']
        print type(deployment), type(topology)
        return render(request, 'oshi/oshi_deployment_details.html',
                      {'deployment': deployment, 'topology_data': json.dumps(topology), 'nodes': topology['vertices'], 'collapsed_sidebar': True})

    except Exception as e:
        print e
        return render(request, 'error.html', {'error_msg': 'Error open project! Please retry.'})

@login_required
def topology_data(request, deployment_id=None):

    topology = {}
    topology_data = OshiParser.importprojectdir('usecases/OSHI/example1', 'json')

    topology = topology_data['oshi']['example1']
    print json.dumps(topology)
    response = HttpResponse(topology, content_type="application/json")
    response["Access-Control-Allow-Origin"] = "*"

    return response

@login_required
def delete_deployment(request, deployment_id=None):
    if request.method == 'POST':

        try:
            #Deployment.objects.filter(id=deployment_id).delete()
            return render(request, 'deployment_delete.html', {})
        except Exception as e:
            print e
            return render(request, 'error.html', {'error_msg': 'Error deleting Deployment.'})

    elif request.method == 'GET':
        try:
            deployments = [] #Deployment.objects.filter(id=deployment_id).select_subclasses()
            deployment_overview = deployments[0].get_overview_data()
            #                 example: 'etsi/etsi_deployment_delete.html'
            #print  prj_token + '/' + prj_token + '_deployment_delete.html', deployment_overview['name']
            return render(request, 'deployment_delete.html',
                          {'deployment_id': deployment_id, 'deployment_name': deployment_overview['name']})

        except Exception as e:
            print e
            return render(request, 'error.html', {'error_msg': 'Deployment not found.'})