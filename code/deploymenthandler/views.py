#
#   Copyright 2017 CNIT - Consorzio Nazionale Interuniversitario per le Telecomunicazioni
#
#   Licensed under the Apache License, Version 2.0 (the "License");
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
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.http import JsonResponse
import json

from sf_user.models import CustomUser
from projecthandler.models import Project
from deploymenthandler.models import DeployAgent, Deployment
from lib.oshi.oshi_parser import OshiParser


def check_not_guest_user(user):
    return not user.is_guest()


@login_required
@permission_required('deploymenthandler', raise_exception=False)
def user_deployments(request):
    raw_content_types = request.META.get('HTTP_ACCEPT', '*/*').split(',')
    result = {}
    options = {
        'creator_id': request.user.id
    }
    for key in ('project_id', 'name', 'deployment_agent', 'project_name'):
        value = request.GET.get(key)
        if value:
            options[key] = value

    deployments = Deployment.objects.filter(**options)
    result.update({'deployments': list(deployments)})
    return __response_handler(request, result, 'deployments_list.html')


@login_required
@permission_required('deploymenthandler', raise_exception=False)
def open_deployment(request, deployment_id=None):
    result = {}
    url = None
    raw_content_types = request.META.get('HTTP_ACCEPT', '*/*').split(',')
    try:
        res_search = Deployment.objects.filter(id=deployment_id)
        if len(res_search) > 0:
            deployment = res_search[0]
            topology_data = OshiParser.importprojectdir('usecases/OSHI/example1', 'json')['oshi']['example1']
            deployment_descriptor = topology_data  ##TODO fix it just developing in OSHI
            url = 'oshi/oshi_deployment_details.html'  ##TODO fix it just developing in OSHI
            if 'application/json' in raw_content_types:
                deployment = json.dumps(deployment.to_json())
            result = {'deployment': deployment, 'topology_data': json.dumps(topology_data),
                      'deployment_descriptor': json.dumps(deployment_descriptor),
                      'collapsed_sidebar': True}
        else:
            url = 'error.html'
            result = {'error_msg': 'Error: Deployment not found.'}

    except Exception as e:
        print e
        url = 'error.html'
        result = {'error_msg': 'Error open deployment! Please retry.'}

    return __response_handler(request, result, url)


@login_required
@permission_required('deploymenthandler', raise_exception=False)
def new_deployment(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name', '')
            start_from = request.POST.get('startfrom')
            if start_from == 'new':
                name_agent = request.POST.get('name_agent', '')
                base_url_agent = request.POST.get('base_url_agent', ' ')
                type_agent = request.POST.get('type_agent', '')
                agent = DeployAgent.objects.create(name=name_agent, base_url=base_url_agent, type=type_agent)
            else:
                agent_id = request.POST.get('agent_id', '')
                agents = DeployAgent.objects.filter(id=agent_id)
                if len(agents) == 0:
                    raise Exception("Agent Not Found")
                agent = agents[0]
                name_agent = agent.name
                base_url_agent = agent.base_url
                type_agent = agent.type
            user = CustomUser.objects.get(id=request.user.id)
            profile = {}
            project_name = request.POST.get('project_name', '')
            project_id = request.POST.get('project_id')

            creator_id = user.id
            status = 'not started'
            new_deployment = Deployment.objects.create(name=name, project_name=project_name, project_id=project_id,
                                                       profile=profile,
                                                        creator_id=creator_id, status=status,
                                                       deployment_agent=agent.to_json())
            # new_deployment.deployment_agent = agent
            new_deployment.save()
            new_deployment.launch()
            url = 'deployment:open_deployment'
        except Exception as e:
            print e
            url = 'error.html'
            result = {'error_msg': 'Error Creating Deployment.'}
            return __response_handler(request, result, url)
    ##TODO fix it with response handler
    return redirect(url, deployment_id=new_deployment.id)


@login_required
@permission_required('deploymenthandler', raise_exception=False)
def monitoring_deployment(request, deployment_id=None):
    res_search = Deployment.objects.filter(id=deployment_id)
    raw_content_types = request.META.get('HTTP_ACCEPT', '*/*').split(',')
    if len(res_search) > 0:
        deployment = res_search[0]
        topology_data = OshiParser.importprojectdir('usecases/OSHI/example1', 'json')
        topology = topology_data['oshi']['example1']
        print "monitor", DeployAgent(deployment.deployment_agent).base_url
        url = 'oshi/oshi_deployment_monitoring.html'
        result = {'deployment': deployment, 'topology_data': json.dumps(topology), 'nodes': topology['vertices'],
                  'collapsed_sidebar': True}
    else:
        url = 'error.html'
        result = {'error_msg': 'Error data monitoring not found.'}
    return __response_handler(request, result, url)


@login_required
@permission_required('deploymenthandler', raise_exception=False)
def delete_deployment(request, deployment_id=None):
    print "delete_deployment", deployment_id
    if request.method == 'POST':
        try:
            Deployment.objects.filter(id=deployment_id).delete()
            url = 'deployment:deployments_list'
            result = {}
        except Exception as e:
            print e
            result = {'error_msg': 'Error deleting Deployment.'}
            url = 'error.html'
        return __response_handler(request, result, url, to_redirect=True)
    elif request.method == 'GET':
        try:
            deployments = Deployment.objects.filter(id=deployment_id)
            deployment = deployments[0]

            return render(request, 'deployment_delete.html',
                          {'deployment': deployment})

        except Exception as e:
            print e
            return render(request, 'error.html', {'error_msg': 'Deployment not found.'})


# Agent Section #####

@login_required
@permission_required('deploymenthandler', raise_exception=False)
def agents_list(request):
    raw_content_types = request.META.get('HTTP_ACCEPT', '*/*').split(',')
    url = None
    result = {}
    try:
        options = {}
        for key in ('type', 'name'):
            value = request.GET.get(key)
            if value:
                options[key] = value
        agents = DeployAgent.objects.filter(**options).values()
        if 'application/json' in raw_content_types:

            result = {'agents': list(agents), 'agent_type': options['type'] if 'type' in options else None}
        else:
            project_types = Project.get_project_types()
            url = 'agents/agents_list.html'
            result = {'agents': list(agents), 'agent_type': options['type'] if 'type' in options else None,
                      'data_type_selector': project_types}

    except Exception as e:
        print e
        url = 'error.html'
        result = {'error_msg': 'Agents not found.'}

    return __response_handler(request, result, url)


@login_required
@permission_required('deploymenthandler', raise_exception=False)
def new_agent(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name', '')
            base_url = request.POST.get('base_url', ' ')
            type = request.POST.get('type', '')
            DeployAgent.objects.create(name=name, base_url=base_url, type=type)
        except Exception as e:
            print e
            url = 'error.html'
            result = {'error_msg': 'Error creating ' + type + ' Agent! Please retry.'}
            return __response_handler(request, result, url)
        return redirect('agent:agents_list')


@login_required
@permission_required('deploymenthandler', raise_exception=False)
def delete_agent(request, agent_id=None):
    try:
        DeployAgent.objects.filter(id=agent_id).delete()
    except Exception as e:
        print e
        url = 'error.html'
        result = {'error_msg': 'Error deleting ' + agent_id + ' Agent! Please retry.'}
        return __response_handler(request, result, url)
    return redirect('agent:agents_list')


def __response_handler(request, data_res, url=None, to_redirect=None):
    raw_content_types = request.META.get('HTTP_ACCEPT', '*/*').split(',')
    if 'application/json' in raw_content_types:
        return JsonResponse(data_res)
    elif to_redirect:
        return redirect(url)
    else:
        return render(request, url, data_res)
