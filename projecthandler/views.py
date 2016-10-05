from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.middleware.csrf import get_token
from projecthandler.models import Project
from sf_user.models import CustomUser
from lib.emparser.util import Util
from lib.emparser.t3d_util import T3DUtil
from lib.emparser import emparser
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import json

import jsonfield
# Create your views here.


def home(request):

    return render(request, 'home.html', {})

def create_project(request): #TODO remove test
    csrf_token_value = get_token(request)

    user = CustomUser.objects.get(id=request.user.id)
    jsonField = jsonfield.JSONField()
    projects = Project.objects.create(name="Prova1", owner=user, validated=True)

    return JsonResponse({'html': []});


def create_new_project(request):

    if request.method == 'POST':
        user = CustomUser.objects.get(id=request.user.id)
        name =request.POST.get('name', '')
        info = request.POST.get('info', '')
        try:
            data_project = emparser.importproject('/Users/francesco/Workspace/sf_t3d/sf_dev/examples/my_example/JSON',
                                             'json')
            print data_project
            project = Project.objects.create(name=name, owner=user, validated=False, info=info, data_project=data_project)

            return render(request, 'new_project.html', {'project_id': project.id})
        except Exception as e:
            print e
            return render(request, 'new_project.html', {'error_msg': 'Error creating project! Please retry.'})

    elif request.method == 'GET':
        csrf_token_value = get_token(request)
        return render(request, 'new_project.html', {})


def user_projects(request):
    csrf_token_value = get_token(request)
    user = CustomUser.objects.get(id=request.user.id)
    projects = Project.objects.filter(owner=user)

    #print list(projects)
    html = render_to_string('projectlist.html', {
        'projects': list(projects),
        "csrf_token_value": csrf_token_value
    })
    #if request.is_ajax():
    return JsonResponse({'html': html});

def open_project(request, project_id = None):
    print project_id
    try:
        projects = Project.objects.filter(id=project_id)
        project_overview = projects[0].get_overview_data()
        return render(request, 'project_details.html', {'project_overview': project_overview, 'project_id': project_id})
    except Exception as e: ##TODO error page
        return render(request, 'error.html', {'project_overview': {}, 'project_id': project_id})


def edit_descriptor(request, project_id = None, descriptor_id = None, descriptor_type = None):
    print project_id, descriptor_id
    if request.method == 'POST':

        return JsonResponse({'html': 'edit_descriptor'})

    elif request.method == 'GET':
        csrf_token_value = get_token(request)
        projects = Project.objects.filter(id=project_id)
        descriptor = projects[0].get_descriptor(descriptor_id, descriptor_type)
        #print descriptor
        return render(request, 'descriptor_view.html', {'project_id': project_id,'descriptor_id': descriptor_id, 'descriptor': descriptor, 'descriptor_string': json.dumps(descriptor)})

def show_descriptors(request, project_id = None, descriptor_type = None):
    csrf_token_value = get_token(request)
    print "project_id", project_id
    #user = CustomUser.objects.get(id=request.user.id)
    projects = Project.objects.filter(id=project_id)

    return render(request, 'project_descriptors.html', {
        'descriptors': projects[0].get_descriptors(descriptor_type),
        'project_id': project_id,
        "csrf_token_value": csrf_token_value,
        'descriptor_type': descriptor_type
    })

def graph(request, project_id = None):
    csrf_token_value = get_token(request)
    projects = Project.objects.filter(id=project_id)

    return render(request, 'project_graph.html', {'project': projects[0], 'project_id': project_id})

def graph_data(request, project_id = None):
    test_t3d = T3DUtil()
    project = emparser.importproject('/Users/francesco/Workspace/sf_t3d/sf_dev/examples/my_example/JSON', 'json')
    topology = test_t3d.build_graph_from_project(project)
    # print response
    response =  HttpResponse(json.dumps(topology), content_type="application/json")
    response["Access-Control-Allow-Origin"] = "*"
    return response

def downlaod(request, project_id = None):
    #return HttpResponseRedirect(reverse("projets:download", args=[project_id]))
    return JsonResponse({'html': 'downlaod'});