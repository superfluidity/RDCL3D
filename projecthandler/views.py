from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.middleware.csrf import get_token
from projecthandler.models import EtsiManoProject
from sf_user.models import CustomUser
from lib.emparser.util import Util
from lib.emparser.t3d_util import T3DUtil
from lib.emparser import emparser
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
import json



@login_required
def home(request):
    return render(request, 'home.html', {})


@login_required
def create_new_project(request):

    if request.method == 'POST':
        user = CustomUser.objects.get(id=request.user.id)
        name =request.POST.get('name', '')
        info = request.POST.get('info', '')
        try:
            ##FIXME da rimuovere usata solo per develop
            data_project = emparser.importproject('sf_dev/examples/my_example/JSON',
                                             'json')
            project = EtsiManoProject.objects.create(name=name, owner=user, validated=False, info=info, data_project=data_project)

            return render(request, 'new_project.html', {'project_id': project.id})
        except Exception as e:
            print e
            return render(request, 'error.html', {'error_msg': 'Error creating project! Please retry.'})

    elif request.method == 'GET':
        csrf_token_value = get_token(request)
        return render(request, 'new_project.html', {})


@login_required
def user_projects(request):
    csrf_token_value = get_token(request)
    user = CustomUser.objects.get(id=request.user.id)
    projects = EtsiManoProject.objects.filter(owner=user)

    #print list(projects)
    html = render_to_string('projectlist.html', {
        'projects': list(projects),
        "csrf_token_value": csrf_token_value
    })
    #if request.is_ajax():
    return JsonResponse({'html': html});


@login_required
def open_project(request, project_id = None):
    try:
        projects = EtsiManoProject.objects.filter(id=project_id)
        project_overview = projects[0].get_overview_data()
        return render(request, 'project_details.html', {'project_overview': project_overview, 'project_id': project_id})
    except Exception as e:
        print e
        return render(request, 'error.html', {'error_msg': 'Error creating project! Please retry.'})


@login_required
def delete_project(request, project_id = None):
    if request.method == 'POST':

        try:
            EtsiManoProject.objects.filter(id=project_id).delete()
            return render(request, 'project_delete.html', {})
        except Exception as e:
            print e
            return render(request, 'error.html', {'error_msg': 'Error deleting Project.'})

    elif request.method == 'GET':
        try:
            projects = EtsiManoProject.objects.filter(id=project_id)
            print "projects", projects[0]
            project_overview = projects[0].get_overview_data()
            print "project_overview", project_overview
            return render(request, 'project_delete.html', {'project_id': project_id, 'project_name': project_overview['name']})
        except Exception as e:
            print e
            return render(request, 'error.html', {'error_msg': 'Project not found.'})

@login_required
def edit_descriptor(request, project_id = None, descriptor_id = None, descriptor_type = None):
    if request.method == 'POST':

        return JsonResponse({'html': 'edit_descriptor'})

    elif request.method == 'GET':
        csrf_token_value = get_token(request)
        projects = EtsiManoProject.objects.filter(id=project_id)
        descriptor = projects[0].get_descriptor(descriptor_id, descriptor_type)
        utility = Util()
        descriptor_string_json = json.dumps(descriptor)
        descriptor_string_yaml = utility.json2yaml(descriptor)
        #print descriptor
        return render(request, 'descriptor_view.html', {'project_id': project_id,'descriptor_id': descriptor_id, 'descriptor_type': descriptor_type, 'descriptor_strings': { 'descriptor_string_yaml': descriptor_string_yaml, 'descriptor_string_json': descriptor_string_json}})


@login_required
def show_descriptors(request, project_id = None, descriptor_type = None):
    csrf_token_value = get_token(request)
    #user = CustomUser.objects.get(id=request.user.id)
    projects = EtsiManoProject.objects.filter(id=project_id)

    return render(request, 'project_descriptors.html', {
        'descriptors': projects[0].get_descriptors(descriptor_type),
        'project_id': project_id,
        "csrf_token_value": csrf_token_value,
        'descriptor_type': descriptor_type
    })


@login_required
def graph(request, project_id = None):
    csrf_token_value = get_token(request)
    projects = EtsiManoProject.objects.filter(id=project_id)

    return render(request, 'project_graph.html', {'project_id': project_id})


@login_required
def graph_data(request, project_id = None):
    test_t3d = T3DUtil()
    projects = EtsiManoProject.objects.filter(id=project_id)
    project = projects[0].get_dataproject() #emparser.importproject('/Users/francesco/Workspace/sf_t3d/sf_dev/examples/my_example/JSON', 'json')
    topology = test_t3d.build_graph_from_project(project)
    # print response
    response =  HttpResponse(json.dumps(topology), content_type="application/json")
    response["Access-Control-Allow-Origin"] = "*"
    return response


@login_required
def downlaod(request, project_id = None):
    csrf_token_value = get_token(request)
    if request.method == 'POST':
        projects = EtsiManoProject.objects.filter(id=project_id)
        in_memory = projects[0].get_zip_archive()
        #in_memory.seek(0)

        response = HttpResponse(content_type="application/zip")
        response["Content-Disposition"] = "attachment; filename=export_"+ project_id+".zip"
        ret_zip = in_memory.getvalue()
        in_memory.close()
        response.write(ret_zip)
        return response

    elif request.method == 'GET':
        return render(request, 'download_etsi.html', {'project_id': project_id})


@login_required
def delete_descriptor(request, project_id=None, descriptor_type=None, descriptor_id=None):
    print project_id, descriptor_type, descriptor_id
    csrf_token_value = get_token(request)
    projects = EtsiManoProject.objects.filter(id=project_id)
    result = projects[0].delete_descriptor(descriptor_type, descriptor_id)
    return render(request, 'project_descriptors.html', {
        'descriptors': projects[0].get_descriptors(descriptor_type),
        'project_id': project_id,
        "csrf_token_value": csrf_token_value,
        'descriptor_type': descriptor_type,
        'alert_message':{
            'success': result,
            'message': "Delete succeeded!" if result else 'Error in delete'}
    })

@login_required
def new_descriptor(request, project_id=None, descriptor_type=None):
    return render(request, 'descriptor_new.html', {
        'project_id': project_id,
        'descriptor_type':descriptor_type})

@login_required
def create_descriptor(request, project_id=None, descriptor_type=None):
    print request.POST.get('type'), request.POST.get('text')
    csrf_token_value = get_token(request)
    projects = EtsiManoProject.objects.filter(id=project_id)
    result = projects[0].create_descriptor(descriptor_type,request.POST.get('text'), request.POST.get('type'))
    data = {}
    data['data'] =  {
        'descriptors': projects[0].get_descriptors(descriptor_type),
        'project_id': project_id,
        "csrf_token_value": csrf_token_value,
        'descriptor_type': descriptor_type,
        'alert_message': {
            'success': result,
            'message': "Descriptor created" if result else 'Error in creation'}
    }
    data['url'] = '/projects/'+project_id+'/descriptors/'+descriptor_type+'/'
    response = HttpResponse(json.dumps(data), content_type="application/json")
    response["Access-Control-Allow-Origin"] = "*"
    return  response
