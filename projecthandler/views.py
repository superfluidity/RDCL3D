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
from django import forms
import json



@login_required
def home(request):
    return render(request, 'home.html', {})


@login_required
def create_new_project(request):

    if request.method == 'POST':
        user = CustomUser.objects.get(id=request.user.id)
        name =request.POST.get('name', '')
        info = request.POST.get('info', ' ')
        ns_files = request.FILES.getlist('ns_files')
        vnf_files = request.FILES.getlist('vnf_files')
        try:
            if ns_files or vnf_files:
                data_project = emparser.importprojectfile(ns_files, vnf_files)
            else:
                ##FIXME da rimuovere usata solo per develop
                data_project = emparser.importprojectdir('sf_dev/examples/my_example/JSON_NEW',
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
def show_descriptors(request, project_id = None, descriptor_type = None):
    csrf_token_value = get_token(request)
    #user = CustomUser.objects.get(id=request.user.id)
    projects = EtsiManoProject.objects.filter(id=project_id)

    return render(request, 'project_descriptors.html', {
        'descriptors': projects[0].get_descriptors(descriptor_type),
        'project_id': project_id,
        'project_overview_data': projects[0].get_overview_data(),
        "csrf_token_value": csrf_token_value,
        'descriptor_type': descriptor_type
    })


@login_required
def graph(request, project_id = None):
    csrf_token_value = get_token(request)
    projects = EtsiManoProject.objects.filter(id=project_id)

    return render(request, 'project_graph.html', {
        'project_id': project_id,
        'project_overview_data': projects[0].get_overview_data(),
        'collapsed_sidebar': True
    })


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
    projects = EtsiManoProject.objects.filter(id=project_id)
    if request.method == 'POST':
        projects = EtsiManoProject.objects.filter(id=project_id)
        in_memory = projects[0].get_zip_archive()

        response = HttpResponse(content_type="application/zip")
        response["Content-Disposition"] = "attachment; filename=export_"+ project_id+".zip"
        ret_zip = in_memory.getvalue()
        in_memory.close()
        response.write(ret_zip)
        return response

    elif request.method == 'GET':
        return render(request, 'download_etsi.html', {
            'project_id': project_id,
            'project_overview_data': projects[0].get_overview_data(),
        })


@login_required
def delete_descriptor(request, project_id=None, descriptor_type=None, descriptor_id=None):
    print project_id, descriptor_type, descriptor_id
    csrf_token_value = get_token(request)
    projects = EtsiManoProject.objects.filter(id=project_id)
    result = projects[0].delete_descriptor(descriptor_type, descriptor_id)
    return render(request, 'project_descriptors.html', {
        'descriptors': projects[0].get_descriptors(descriptor_type),
        'project_id': project_id,
        'project_overview_data': projects[0].get_overview_data(),
        "csrf_token_value": csrf_token_value,
        'descriptor_type': descriptor_type,
        'alert_message':{
            'success': result,
            'message': "Delete succeeded!" if result else 'Error in delete'}
    })

@login_required
def new_descriptor(request, project_id=None, descriptor_type=None):
    if request.method == 'GET':
        projects = EtsiManoProject.objects.filter(id=project_id)
        return render(request, 'descriptor_new.html', {
            'project_id': project_id,
            'descriptor_type':descriptor_type,
            'project_overview_data': projects[0].get_overview_data(),
        })
    elif request.method == 'POST':
        csrf_token_value = get_token(request)
        projects = EtsiManoProject.objects.filter(id=project_id)
        if(request.POST.get('type') =="file"):
            file = request.FILES['file']
            text = file.read()
            type = file.name.split(".")[-1]
            result = projects[0].create_descriptor(descriptor_type, text, type)
        else:
            result = projects[0].create_descriptor(descriptor_type, request.POST.get('text'), request.POST.get('type'))
        response_data = {
            'project_id': project_id,
            'descriptor_type': descriptor_type,
            'project_overview_data': projects[0].get_overview_data(),
            'alert_message': {
                'success': result,
                'message': "Descriptor created" if result else 'Error in creation'}
            }
        status_code = 200 if result else 500
        response = HttpResponse(json.dumps(response_data), content_type="application/json", status=status_code)
        response["Access-Control-Allow-Origin"] = "*"
        return response


@login_required
def edit_descriptor(request, project_id=None, descriptor_id=None, descriptor_type=None):
    if request.method == 'POST':
        projects = EtsiManoProject.objects.filter(id=project_id)
        result = projects[0].edit_descriptor(descriptor_type, descriptor_id, request.POST.get('text'), request.POST.get('type'))
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
        projects = EtsiManoProject.objects.filter(id=project_id)
        descriptor = projects[0].get_descriptor(descriptor_id, descriptor_type)
        utility = Util()
        descriptor_string_json = json.dumps(descriptor)
        descriptor_string_yaml = utility.json2yaml(descriptor)
        #print descriptor
        return render(request, 'descriptor_view.html', {
            'project_id': project_id,
            'descriptor_id': descriptor_id,
            'project_overview_data': projects[0].get_overview_data(),
            'descriptor_type': descriptor_type,
            'descriptor_strings': { 'descriptor_string_yaml': descriptor_string_yaml, 'descriptor_string_json': descriptor_string_json}})

@login_required
def graph_positions(request, project_id=None):
    if request.method == 'POST':
        projects = EtsiManoProject.objects.filter(id=project_id)
        result = projects[0].edit_graph_positions(json.loads(request.POST.get('positions')))
        status_code = 200 if result else 500
        response = HttpResponse(json.dumps({}), content_type="application/json", status=status_code)
        response["Access-Control-Allow-Origin"] = "*"
        return response

@login_required
def add_element(request, project_id=None):
    if request.method == 'POST':
        result = False
        projects = EtsiManoProject.objects.filter(id=project_id)
        group_id = request.POST.get('group_id')
        element_id = request.POST.get('element_id')
        element_type = request.POST.get('element_type')
        print element_id
        if element_type == 'ns_cp':
            result = projects[0].add_ns_sap(group_id, element_id)
        elif element_type == 'ns_vl':
            result = projects[0].add_ns_vl(group_id, element_id)
        elif element_type == 'vnf':
            result = projects[0].add_ns_vnf(group_id, element_id)
        elif element_type == 'vnf_vl':
            result = projects[0].add_vnf_intvl(group_id, element_id)
        elif element_type == 'vnf_ext_cp':
            result = projects[0].add_vnf_vnfextcpd(group_id, element_id)
        elif element_type == 'vnf_vdu':
            result = projects[0].add_vnf_vdu(group_id, element_id)
        elif element_type == 'vnf_vdu_cp':
            #FixMe it should call projects[0].add_vnf_vducp(vnf_id, vdu_id, vducp_id)
            result = True
        status_code = 200 if result else 500
        response = HttpResponse(json.dumps({}), content_type="application/json", status=status_code)
        response["Access-Control-Allow-Origin"] = "*"
        return response

@login_required
def remove_element(request, project_id=None):
    if request.method == 'POST':
        result = False
        projects = EtsiManoProject.objects.filter(id=project_id)
        group_id = request.POST.get('group_id')
        element_id = request.POST.get('element_id')
        element_type = request.POST.get('element_type')
        print element_id
        if element_type == 'ns_cp':
            result = projects[0].remove_ns_sap(group_id, element_id)
        elif element_type == 'ns_vl':
            result = projects[0].remove_ns_vl(group_id, element_id)
        elif element_type == 'vnf':
            result = projects[0].remove_ns_vnf(group_id, element_id)
        elif element_type == 'vnf_vl':
            result = projects[0].remove_vnf_intvl(group_id, element_id)
        elif element_type == 'vnf_ext_cp':
            result = projects[0].remove_vnf_vnfextcpd(group_id, element_id)
        elif element_type == 'vnf_vdu':
            result = projects[0].remove_vnf_vdu(group_id, element_id)
        elif element_type == 'vnf_vdu_cp':
            #FixMe it should call projects[0].remove_vnf_vducp(vnf_id, vdu_id, vducp_id)
            result = True
        status_code = 200 if result else 500
        response = HttpResponse(json.dumps({}), content_type="application/json", status=status_code)
        response["Access-Control-Allow-Origin"] = "*"
        return response

@login_required
def add_link(request, project_id=None):
    if request.method == 'POST':
        result = False
        projects = EtsiManoProject.objects.filter(id=project_id)
        source = json.loads(request.POST.get('source'))
        destination = json.loads(request.POST.get('destination'))
        source_type = source['info']['type']
        destination_type = destination['info']['type']
        if (source_type, destination_type) in [('ns_vl', 'ns_cp'), ('ns_cp', 'ns_vl')]:
            vl_id = source['id'] if source_type == 'ns_vl' else destination['id']
            sap_id = source['id'] if source_type == 'ns_cp' else destination['id']
            result = projects[0].link_vl_sap(source['info']['group'],vl_id, sap_id)
        elif (source_type, destination_type) in [('ns_vl', 'ns_vnf'), ('ns_vnf', 'ns_vl')]:
            #FixMe it should call projects[0].link_vl_vnf(ns_id, vl_id, vnf_id, ext_cp_id)
            result = True
        elif (source_type, destination_type) in [('vnf_vl', 'vnf_vdu_cp'), ('vnf_vdu_cp', 'vnf_vl')]:
            #FixMe it should call projects[0].link_vducp_intvl(vnf_id, vdu_id, vducp_id, intvl_id)
            result = True
        if (source_type, destination_type) in [('vnf_ext_cp', 'vnf_vl'), ('vnf_vl', 'vnf_ext_cp')]:
            vnfExtCpd_id = source['id'] if source_type == 'vnf_ext_cp' else destination['id']
            intvl_id = source['id'] if source_type == 'vnf_vl' else destination['id']
            result = projects[0].link_vnfextcpd_intvl(source['info']['group'], vnfExtCpd_id, intvl_id)
        status_code = 200 if result else 500
        response = HttpResponse(json.dumps({}), content_type="application/json", status=status_code)
        response["Access-Control-Allow-Origin"] = "*"
        return response