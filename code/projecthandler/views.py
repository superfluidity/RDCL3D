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

import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from lib.util import Util
from sf_user.models import CustomUser

# DO NOT REMOVE THIS COMMENT #
# Project Models #
from projecthandler.cran_model import CranProject
from projecthandler.toscanfv_model import ToscanfvProject
from projecthandler.superfluidity_model import SuperfluidityProject
from projecthandler.oshi_model import OshiProject
from projecthandler.click_model import ClickProject
from projecthandler.etsi_model import EtsiProject
from projecthandler.models import Project
from projecthandler.tosca_model import ToscaProject

# DO NOT REMOVE THIS COMMENT #
# Project Model Type declarations #
Project.add_project_type('cran', CranProject)
Project.add_project_type('toscanfv', ToscanfvProject)
Project.add_project_type('superfluidity', SuperfluidityProject)
Project.add_project_type('oshi', OshiProject)
Project.add_project_type('etsi', EtsiProject)
Project.add_project_type('click', ClickProject)
Project.add_project_type('tosca', ToscaProject)

@login_required
def home(request):
    return render(request, 'home.html', {})


@login_required
def create_new_project(request):
    if request.method == 'POST':
        error_msgs = []
        user = CustomUser.objects.get(id=request.user.id)
        name = request.POST.get('name', 'WithoutName')
        info = request.POST.get('info', ' ')
        type = request.POST.get('type', '')
        start_from = request.POST.get('startfrom', 'scratch')

        project_types = Project.get_project_types()
        if type in project_types:
            project_class = project_types[type]

        else:
            # FIXME this error is not handled
            error_msgs.append('Project type undefined.')
            return render(request, 'error.html',
                          {'error_msg': 'Error creating new project, project type undefined. Please retry.'})

        try:

            if start_from == 'scratch':
                print 'from scratch'
                data_project = {}

            elif start_from == 'files':
                print 'from files'
                data_project = project_class.data_project_from_files(request)

            elif start_from == 'example':
                print 'from example'
                data_project = project_class.data_project_from_example(request)

            project = project_class.create_project(name, user, False, info, data_project)
            # print project.get_dataproject()


        except Exception as e:
            print 'Error creating ' + type + ' project! Please retry.'
            print e
            return render(request, 'error.html', {'error_msg': 'Error creating ' + type + ' project! Please retry.'})
        return redirect('projects:open_project', project_id=project.id)

    elif request.method == 'GET':
        csrf_token_value = get_token(request)
        result = {}
        data_type_selector = [{
            'id': '-1',
            'text': 'Select an option'
        }]
        type_example_files = {}
        type_container_template = ''
        project_types = Project.get_project_types()
        print "project_types", project_types.keys()
        for type in project_types:
            project_class = project_types[type]
            type_example_files.update(project_class.get_example_list())
            data_type_selector.append({
                'id': type,
                'text': type,
                'value': type
            })
            type_container_template += render_to_string(type + '/' + type + '_new_project.html')

        result.update({'type_example_files': json.dumps(type_example_files)})
        result.update({'data_type_selector': json.dumps(data_type_selector)})
        result.update({'type_container_template': type_container_template})
        result.update({'csrf_token': csrf_token_value})
        return render(request, 'new_project.html', result)


@login_required
def user_projects(request):
    csrf_token_value = get_token(request)
    user = CustomUser.objects.get(id=request.user.id)
    projects = Project.objects.filter(owner=user).select_subclasses()

    # print list(projects)
    #html = render_to_string('projectlist.html', {
    #    'projects': list(projects),
    #    'csrf_token': csrf_token_value
    #})
    # if request.is_ajax():
    return render(request, 'projectlist.html', {
        'projects': list(projects),
        'csrf_token': csrf_token_value
    })
    #return JsonResponse({'html': html});


@login_required
def open_project(request, project_id=None):
    try:
        projects = Project.objects.filter(id=project_id).select_subclasses()
        project_overview = projects[0].get_overview_data()
        prj_token = project_overview['type']
        return render(request, prj_token + '/' + prj_token + '_project_details.html',
                      {'project_overview': project_overview, 'project_id': project_id})

    except Exception as e:
        print e
        return render(request, 'error.html', {'error_msg': 'Error open project! Please retry.'})


@login_required
def delete_project(request, project_id=None):
    if request.method == 'POST':

        try:
            Project.objects.filter(id=project_id).delete()
            return render(request, 'project_delete.html', {})
        except Exception as e:
            print e
            return render(request, 'error.html', {'error_msg': 'Error deleting Project.'})

    elif request.method == 'GET':
        try:
            projects = Project.objects.filter(id=project_id).select_subclasses()
            project_overview = projects[0].get_overview_data()
            prj_token = project_overview['type']
            #                 example: 'etsi/etsi_project_delete.html'
            print  prj_token + '/' + prj_token + '_project_delete.html', project_overview['name']
            return render(request, prj_token + '/' + prj_token + '_project_delete.html',
                          {'project_id': project_id, 'project_name': project_overview['name']})

        except Exception as e:
            print e
            return render(request, 'error.html', {'error_msg': 'Project not found.'})


@login_required
def show_descriptors(request, project_id=None, descriptor_type=None):
    csrf_token_value = get_token(request)
    projects = Project.objects.filter(id=project_id).select_subclasses()
    project_overview = projects[0].get_overview_data()
    prj_token = project_overview['type']

    page = prj_token + '/' + prj_token + '_project_descriptors.html'

    return render(request, page, {
        'descriptors': projects[0].get_descriptors(descriptor_type),
        'project_id': project_id,
        'project_type': prj_token,
        'project_overview_data': project_overview,
        "csrf_token_value": csrf_token_value,
        'descriptor_type': descriptor_type
    })


@login_required
def graph(request, project_id=None):
    if request.method == 'GET':
        csrf_token_value = get_token(request)
        projects = Project.objects.filter(id=project_id).select_subclasses()
        project_overview = projects[0].get_overview_data()
        prj_token = project_overview['type']
        # example : 'etsi/project_graph.html'
        return render(request, prj_token + '/project_graph.html', {
            'project_id': project_id,
            'project_overview_data': projects[0].get_overview_data(),
            'collapsed_sidebar': True
        })


@login_required
def graph_data(request, project_id=None, descriptor_id=None):
    projects = Project.objects.filter(id=project_id).select_subclasses()
    project_overview = projects[0].get_overview_data()
    # data = projects[0].get_overview_data()
    prj_token = project_overview['type']

    topology = projects[0].get_graph_data_json_topology(descriptor_id)
    response = HttpResponse(topology, content_type="application/json")
    response["Access-Control-Allow-Origin"] = "*"

    return response


@login_required
def download(request, project_id=None):
    csrf_token_value = get_token(request)
    projects = Project.objects.filter(id=project_id).select_subclasses()
    if request.method == 'POST':
        # projects = EtsiProject.objects.filter(id=project_id)
        in_memory = projects[0].get_zip_archive()

        response = HttpResponse(content_type="application/zip")
        response["Content-Disposition"] = "attachment; filename=export_" + project_id + ".zip"
        ret_zip = in_memory.getvalue()
        in_memory.close()
        response.write(ret_zip)
        return response

    elif request.method == 'GET':
        return render(request, 'download.html', {
            'project_id': project_id,
            'project_overview_data': projects[0].get_overview_data(),
        })


@login_required
def delete_descriptor(request, project_id=None, descriptor_type=None, descriptor_id=None):
    csrf_token_value = get_token(request)
    projects = Project.objects.filter(id=project_id).select_subclasses()
    result = projects[0].delete_descriptor(descriptor_type, descriptor_id)
    project_overview = projects[0].get_overview_data()
    prj_token = project_overview['type']
    page = prj_token + '/' + prj_token + '_project_descriptors.html'
    # if project_overview['type'] == 'etsi':
    #     page = 'etsi/etsi_project_descriptors.html'
    # elif project_overview['type'] == 'click':
    #     page = 'click/click_project_descriptors.html'
    return render(request, page, {
        'descriptors': projects[0].get_descriptors(descriptor_type),
        'project_id': project_id,
        'project_overview_data': project_overview,
        "csrf_token_value": csrf_token_value,
        'descriptor_type': descriptor_type,
        'alert_message': {
            'success': result,
            'message': "Delete succeeded!" if result else 'Error in delete'}
    })


@login_required
def clone_descriptor(request, project_id=None, descriptor_type=None, descriptor_id=None):
    csrf_token_value = get_token(request)
    projects = Project.objects.filter(id=project_id).select_subclasses()
    new_id = request.GET.get('newid', '')
    result = projects[0].clone_descriptor(descriptor_type, descriptor_id, new_id)
    project_overview = projects[0].get_overview_data()
    prj_token = project_overview['type']
    page = prj_token + '/' + prj_token + '_project_descriptors.html'
    # if project_overview['type'] == 'etsi':
    #     page = 'etsi/etsi_project_descriptors.html'
    # elif project_overview['type'] == 'click':
    #     page = 'click/click_project_descriptors.html'
    return render(request, page, {
        'descriptors': projects[0].get_descriptors(descriptor_type),
        'project_id': project_id,
        'project_overview_data': project_overview,
        "csrf_token_value": csrf_token_value,
        'descriptor_type': descriptor_type,
        'alert_message': {
            'success': result,
            'message': "Cloned!" if result else 'Error in cloning'}
    })


@login_required
def new_descriptor(request, project_id=None, descriptor_type=None):
    projects = Project.objects.filter(id=project_id).select_subclasses()
    project_overview = projects[0].get_overview_data()
    prj_token = project_overview['type']
    page = prj_token + '/descriptor/descriptor_new.html'
    if request.method == 'GET':
        request_id = request.GET.get('id', '')

        json_template = projects[0].get_new_descriptor(descriptor_type, request_id)
        print 'new descriptor GET', json_template

        descriptor_string_yaml = Util.json2yaml(json_template)
        descriptor_string_json = json.dumps(json_template)

        return render(request, page, {
            'project_id': project_id,
            'descriptor_type': descriptor_type,
            'descriptor_id': request_id,
            'project_overview_data': project_overview,
            'descriptor_strings': {'descriptor_string_yaml': descriptor_string_yaml,
                                   'descriptor_string_json': descriptor_string_json}
        })
    elif request.method == 'POST':
        csrf_token_value = get_token(request)
        data_type = request.POST.get('type')
        if data_type == "file":
            file_uploaded = request.FILES['file']
            text = file_uploaded.read()
            data_type = file_uploaded.name.split(".")[-1]
            desc_name = file_uploaded.name.split(".")[0]

        else:
            text = request.POST.get('text')
            desc_name = request.POST.get('id')
        result = projects[0].create_descriptor(desc_name, descriptor_type, text, data_type)

        response_data = {
            'project_id': project_id,
            'descriptor_type': descriptor_type,
            'project_overview_data': projects[0].get_overview_data(),
            'descriptor_id': result,
            'alert_message': {
                'success': True if result != False else False,
                'message': "Descriptor created" if result else 'Error in creation'}
        }
        status_code = 200 if result != False else 500
        response = HttpResponse(json.dumps(response_data), content_type="application/json", status=status_code)
        response["Access-Control-Allow-Origin"] = "*"
        return response


@login_required
def edit_descriptor(request, project_id=None, descriptor_id=None, descriptor_type=None):
    if request.method == 'POST':
        print "edit_descriptor"
        projects = Project.objects.filter(id=project_id).select_subclasses()
        result = projects[0].edit_descriptor(descriptor_type, descriptor_id, request.POST.get('text'),
                                             request.POST.get('type'))
        response_data = {
            'project_id': project_id,
            'descriptor_type': descriptor_type,
            'project_overview_data': projects[0].get_overview_data(),
            'alert_message': {
                'success': result,
                'message': "Descriptor modified." if result else 'Error during descriptor editing.'}
        }
        status_code = 200 if result else 500
        response = HttpResponse(json.dumps(response_data), content_type="application/json", status=status_code)
        response["Access-Control-Allow-Origin"] = "*"
        return response

    elif request.method == 'GET':
        csrf_token_value = get_token(request)
        projects = Project.objects.filter(id=project_id).select_subclasses()
        project_overview = projects[0].get_overview_data()
        print project_overview
        prj_token = project_overview['type']
        page = prj_token + '/descriptor/descriptor_view.html'

        descriptor = projects[0].get_descriptor(descriptor_id, descriptor_type)

        descriptor_string_json = json.dumps(descriptor)
        descriptor_string_yaml = Util.json2yaml(descriptor)
        # print descriptor
        return render(request, page, {
            'project_id': project_id,
            'descriptor_id': descriptor_id,
            'project_overview_data': projects[0].get_overview_data(),
            'descriptor_type': descriptor_type,
            'descriptor_strings': {'descriptor_string_yaml': descriptor_string_yaml,
                                   'descriptor_string_json': descriptor_string_json}})


@login_required
def graph_positions(request, project_id=None):
    if request.method == 'POST':
        projects = Project.objects.filter(id=project_id).select_subclasses()
        result = projects[0].edit_graph_positions(json.loads(request.POST.get('positions')))
        status_code = 200 if result else 500
        response = HttpResponse(json.dumps({}), content_type="application/json", status=status_code)
        response["Access-Control-Allow-Origin"] = "*"
        return response


@login_required
def add_element(request, project_id=None):
    if request.method == 'POST':
        projects = Project.objects.filter(id=project_id).select_subclasses()
        result = projects[0].get_add_element(request)

        status_code = 200 if result else 500
        response = HttpResponse(json.dumps({}), content_type="application/json", status=status_code)
        response["Access-Control-Allow-Origin"] = "*"
        return response


@login_required
def remove_element(request, project_id=None):
    if request.method == 'POST':
        projects = Project.objects.filter(id=project_id).select_subclasses()
        result = projects[0].get_remove_element(request)

        status_code = 200 if result else 500
        response = HttpResponse(json.dumps({}), content_type="application/json", status=status_code)
        response["Access-Control-Allow-Origin"] = "*"
        return response


@login_required
def add_link(request, project_id=None):
    if request.method == 'POST':
        projects = Project.objects.filter(id=project_id).select_subclasses()
        result = projects[0].get_add_link(request)

        status_code = 200 if result else 500
        response = HttpResponse(json.dumps({}), content_type="application/json", status=status_code)
        response["Access-Control-Allow-Origin"] = "*"
        return response


@login_required
def remove_link(request, project_id=None):
    if request.method == 'POST':
        projects = Project.objects.filter(id=project_id).select_subclasses()
        result = projects[0].get_remove_link(request)

        status_code = 200 if result else 500
        response = HttpResponse(json.dumps({}), content_type="application/json", status=status_code)
        response["Access-Control-Allow-Origin"] = "*"
        return response

@login_required
def get_available_nodes(request, project_id=None):
    if request.method == 'GET':
        csrf_token_value = get_token(request)
        projects = Project.objects.filter(id=project_id).select_subclasses()
        print "get_available_nodes", request.GET.dict()
        result = projects[0].get_available_nodes(request.GET.dict())
        status_code = 500 if result == None else 200
        print json.dumps(result)
        response = HttpResponse(json.dumps(result), content_type="application/json", status=status_code)
        response["Access-Control-Allow-Origin"] = "*"
        return response

@login_required
def overviewelement(request, project_id=None):
    if request.method == 'GET':
        result = {}
        error_msg = None
        try:
            projects = Project.objects.filter(id=project_id).select_subclasses()
            project = projects[0]
            parameters = request.GET.dict()
            print "parameters", parameters
            result = project.get_node_overview(**parameters)
        except Exception as e:
            error_msg = str(e)

        if error_msg is not None:
            return JsonResponse({'error': {'error_msg': str(error_msg)}})

        return JsonResponse({'node_overview': result})

# ETSI specific method #
@login_required
def add_node_to_vnffg(request, project_id=None):
    print "add_node_to_vnffg"  # TODO log
    if request.method == 'POST':
        projects = Project.objects.filter(id=project_id).select_subclasses()
        result = projects[0].add_node_to_vnffg(request)

        status_code = 200 if result else 500
        response = HttpResponse(json.dumps({}), content_type="application/json", status=status_code)
        response["Access-Control-Allow-Origin"] = "*"
        return response


@login_required
def unused_vnf(request, project_id=None, nsd_id=None):
    if request.method == 'GET':
        print 'in method unused_vnf : ', project_id, nsd_id  # TODO log
        projects = Project.objects.filter(id=project_id).select_subclasses()
        result = projects[0].get_unused_vnf(nsd_id)
        status_code = 500 if result == None else 200
        response = HttpResponse(json.dumps(result), content_type="application/json", status=status_code)
        response["Access-Control-Allow-Origin"] = "*"
        return response

# end ETSI specific method #


# TOSCA specific method #
@login_required
def generatehottemplate(request, project_id=None, project=None, descriptor_id=None, descriptor_type=None):
    """It is one of the custom_action methods
        Heat Orchestration Template
    NB The project is already extracted from project_id in the generic custom_action method
    """
    result = {}
    error_msg = None
    try:
        result = project.get_generatehotemplate(request, descriptor_id, descriptor_type)
    except Exception as e:
        error_msg = e

    if error_msg is not None:
        return JsonResponse({'error': {'error_msg': str(error_msg)}})

    return JsonResponse({'hot':  str(result)})

# end TOSCA specific method #


@login_required
def custom_action(request, project_id=None, descriptor_id=None, descriptor_type=None, action_name=None):
    if request.method == 'GET':
        projects = Project.objects.filter(id=project_id).select_subclasses()
        print "Custom action: " + action_name
        return globals()[action_name](request, project_id, projects[0], descriptor_id, descriptor_type)
