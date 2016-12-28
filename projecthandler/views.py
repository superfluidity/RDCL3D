import json
from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.middleware.csrf import get_token
from sf_user.models import CustomUser
from lib.etsiparser.util import Util
# from lib.etsiparser.t3d_util import rdcl3d_util
#from lib.etsiparser import etsiparser
from lib.clickparser import mainrdcl
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from projecthandler.models import Project
from projecthandler.etsi_model import EtsiProject
from projecthandler.click_model import ClickProject

Project.add_project_type('etsi', EtsiProject)
Project.add_project_type('click', ClickProject)


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

        # if type == 'etsi':
        #     project_class = EtsiProject
        # elif type == 'click':
        #     project_class = ClickProject
        else:
            #FIXME this error is not handled 
            error_msgs.push('Project type undefined.')


        try:

        # if type == 'etsi':

            if start_from == 'scratch':
                data_project = {}

            elif start_from == 'files':
                # data_project = EtsiProject.data_project_from_files(request)
                data_project = project_class.data_project_from_files(request)

            #     ns_files = request.FILES.getlist('ns_files')
            #     vnf_files = request.FILES.getlist('vnf_files')
            #     if ns_files or vnf_files:
            #         data_project = etsiparser.importprojectfile(ns_files, vnf_files)

            elif start_from == 'example':
                # data_project = EtsiProject.data_project_from_example(request)
                data_project = project_class.data_project_from_example(request)

                # example_id = request.POST.get('example-etsi-id', '')
                # data_project = etsiparser.importprojectdir('usecases/ETSI/' + example_id + '/JSON', 'json')

            
            # project = EtsiProject.create_project (name, user, False, info, data_project)
            project = project_class.create_project (name, user, False, info, data_project)

            # project = EtsiProject.objects.create (name=name, owner=user, validated=False, info=info,
            #                                          data_project=data_project)

        # elif type == 'click':

        #     if start_from == 'files':
        #         cfg_files = request.FILES.getlist('cfg_files')
        #         data_project = mainrdcl.importprojectfile(cfg_files)
        #     elif start_from == 'example':
        #         ##FIXME
        #         example_id = request.POST.get('example-click-id', '')
        #         data_project = {}
        #     project = ClickProject.objects.create(name=name, owner=user, validated=False, info=info,
        #                                           data_project=data_project)
        # else:
        #     error_msgs.push('Project type undefined.')

        except Exception as e:
            print 'Error creating '+type+' project! Please retry.'
            print e
            return render(request, 'error.html', {'error_msg': 'Error creating '+type+' project! Please retry.'})

        return render(request, 'new_project.html', {'project_id': project.id})

    elif request.method == 'GET':
        csrf_token_value = get_token(request)
        
        examples_by_type = {}
        
        project_types = Project.get_project_types()
        for type in project_types:
            project_class = project_types[type]
            examples_by_type.update(project_class.get_example_list())


        return render(request, 'new_project.html', examples_by_type)
        # return render(request, 'new_project.html', {'etsi_example': Util().get_etsi_example_list(),
        #                                             'click_example': Util().get_click_example_list()})


@login_required
def user_projects(request):
    csrf_token_value = get_token(request)
    user = CustomUser.objects.get(id=request.user.id)
    projects = Project.objects.filter(owner=user).select_subclasses()

    # print list(projects)
    html = render_to_string('projectlist.html', {
        'projects': list(projects),
        "csrf_token_value": csrf_token_value
    })
    # if request.is_ajax():
    return JsonResponse({'html': html});


@login_required
def open_project(request, project_id=None):
    try:
        projects = Project.objects.filter(id=project_id).select_subclasses()
        project_overview = projects[0].get_overview_data()
        prj_token = project_overview['type']
        #                      example: 'etsi/etsi_project_details.html'
        return render(request, prj_token+'/'+prj_token+'_project_details.html',
                          {'project_overview': project_overview, 'project_id': project_id})
        # if project_overview['type'] == 'etsi':
        #     return render(request, 'etsi/etsi_project_details.html',
        #                   {'project_overview': project_overview, 'project_id': project_id})
        # elif project_overview['type'] == 'click':
        #     return render(request, 'click/click_project_details.html',
        #                   {'project_overview': project_overview, 'project_id': project_id})

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
            return render(request, prj_token+'/'+prj_token+'_project_delete.html',
                              {'project_id': project_id, 'project_name': project_overview['name']})
            # if project_overview['type'] == 'etsi':
            #     return render(request, 'etsi/etsi_project_delete.html',
            #                   {'project_id': project_id, 'project_name': project_overview['name']})
            # elif project_overview['type'] == 'click':
            #     return render(request, 'click/click_project_delete.html',
            #                   {'project_id': project_id, 'project_name': project_overview['name']})

        except Exception as e:
            print e
            return render(request, 'error.html', {'error_msg': 'Project not found.'})


@login_required
def show_descriptors(request, project_id=None, descriptor_type=None):
    csrf_token_value = get_token(request)
    projects = Project.objects.filter(id=project_id).select_subclasses()
    project_overview = projects[0].get_overview_data()
    prj_token = project_overview['type']

    page = prj_token+'/'+prj_token+'_project_descriptors.html'
    # if project_overview['type'] == 'etsi':
    #     page = 'etsi/etsi_project_descriptors.html'

    # elif project_overview['type'] == 'click':
    #     page = 'click/click_project_descriptors.html'

    return render(request, page, {
        'descriptors': projects[0].get_descriptors(descriptor_type),
        'project_id': project_id,
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
        return render(request, prj_token+'/project_graph.html', {
            'project_id': project_id,
            'project_overview_data': projects[0].get_overview_data(),
            'collapsed_sidebar': True
        })

        # type = request.GET.get('type')
        # if type == 'ns' or type == 'vnf': # questo va sostituito con un if a livello di project type a breve, e poi sostituito con una cosa parametrica come sopra 
        #     csrf_token_value = get_token(request)
        #     projects = Project.objects.filter(id=project_id).select_subclasses()
        #     return render(request, 'etsi/project_graph.html', {
        #         'project_id': project_id,
        #         'project_overview_data': projects[0].get_overview_data(),
        #         'collapsed_sidebar': True
        #     })

        # elif type == 'click':
        #     csrf_token_value = get_token(request)
        #     projects = Project.objects.filter(id=project_id).select_subclasses()
        #     return render(request, 'click/click_project_graph.html', {
        #         'project_id': project_id,
        #         'project_overview_data': projects[0].get_overview_data(),
        #         'collapsed_sidebar': True
        #     })


@login_required
def graph_data(request, project_id=None, descriptor_id=None):
    projects = Project.objects.filter(id=project_id).select_subclasses()
    project_overview = projects[0].get_overview_data()
    # data = projects[0].get_overview_data()
    prj_token = project_overview['type']

    topology = projects[0].get_graph_data_json_topology(descriptor_id)
    response = HttpResponse(topology, content_type="application/json")
    response["Access-Control-Allow-Origin"] = "*"

    # if prj_token == 'etsi':
    #     test_t3d = rdcl3d_util()
    #     project = projects[0].get_dataproject()
    #     topology = test_t3d.build_graph_from_project(project)
    #     # print response
    #     response = HttpResponse(json.dumps(topology), content_type="application/json")
    #     response["Access-Control-Allow-Origin"] = "*"
    # elif prj_token == 'click':
    #     project = projects[0].get_descriptor(descriptor_id, prj_token)
    #     topology = mainrdcl.importprojectjson(project)
    #     response = HttpResponse(topology, content_type="application/json")
    #     response["Access-Control-Allow-Origin"] = "*"
    
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
        return render(request, 'download_etsi.html', {  #TODO REFACTOR
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
    page = prj_token+'/'+prj_token+'_project_descriptors.html'
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
    page = prj_token+'/'+prj_token+'_project_descriptors.html'
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
    page = prj_token+'/descriptor/descriptor_new.html'
    if request.method == 'GET':
        request_id = request.GET.get('id', '')

        util = Util()

        json_template = projects[0].get_new_descriptor(descriptor_type, request_id)

        # if prj_token == 'etsi':
        #     # page = 'etsi/descriptor/descriptor_new.html'

        #     json_template = util.get_descriptor_template(descriptor_type)
        #     if descriptor_type == 'nsd':
        #         json_template['nsdIdentifier'] = request_id
        #         json_template['nsdInvariantId'] = request_id
        #     else:
        #         json_template['vnfdId'] = request_id

        # elif prj_token == 'click':
        #     # page = 'click/descriptor/descriptor_new.html'
        #     json_template = ''

        descriptor_string_yaml = util.json2yaml(json_template)
        descriptor_string_json = json.dumps(json_template)

        return render(request, page, {
            'project_id': project_id,
            'descriptor_type': descriptor_type,
            'project_overview_data': project_overview,
            'descriptor_strings': {'descriptor_string_yaml': descriptor_string_yaml,
                                   'descriptor_string_json': descriptor_string_json}
        })
    elif request.method == 'POST':
        csrf_token_value = get_token(request)
        if request.POST.get('type') == "file":
            file = request.FILES['file']
            text = file.read()
            type = file.name.split(".")[-1]
        else:
            text = request.POST.get('text')
            type = request.POST.get('type')
            desc_name = request.POST.get('it')  #TODO capire 'it' che significa ???

        result = projects[0].create_descriptor(desc_name, descriptor_type, text, type)

        # if prj_token == 'etsi':
        #     result = projects[0].create_descriptor(descriptor_type, text, type)
        # elif prj_token == 'click':
        #     result = projects[0].create_descriptor(desc_name, descriptor_type, text, type)
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
        prj_token = project_overview['type']
        page = prj_token+'/descriptor/descriptor_view.html'

        descriptor = projects[0].get_descriptor(descriptor_id, descriptor_type)
        # if project_overview['type'] == 'etsi':
        #     page = 'etsi/descriptor/descriptor_view.html'
        # elif project_overview['type'] == 'click':
        #     page = 'click/descriptor/descriptor_view.html'
        utility = Util()
        descriptor_string_json = json.dumps(descriptor)
        descriptor_string_yaml = utility.json2yaml(descriptor)
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
def unused_vnf(request, project_id=None, nsd_id=None):
    if request.method == 'GET':
        print 'in method unused_vnf : ',project_id, nsd_id #TODO log
        projects = Project.objects.filter(id=project_id).select_subclasses()
        result = projects[0].get_unused_vnf(nsd_id)
        status_code = 500 if result == None else 200
        response = HttpResponse(json.dumps(result), content_type="application/json", status=status_code)
        response["Access-Control-Allow-Origin"] = "*"
        return response


@login_required
def add_element(request, project_id=None):
    if request.method == 'POST':
        #result = False
        # projects = EtsiProject.objects.filter(id=project_id)
        projects = Project.objects.filter(id=project_id).select_subclasses()
        result = projects[0].get_add_element(request)

        # group_id = request.POST.get('group_id')
        # element_id = request.POST.get('element_id')
        # element_type = request.POST.get('element_type')
        # existing_vnf = request.POST.get('existing_vnf')
        # if element_type == 'ns_cp':
        #     result = projects[0].add_ns_sap(group_id, element_id)
        # elif element_type == 'ns_vl':
        #     result = projects[0].add_ns_vl(group_id, element_id)
        # elif element_type == 'vnf':
        #     if existing_vnf == 'true':
        #         result = projects[0].add_ns_existing_vnf(group_id, element_id)
        #     else:
        #         result = projects[0].add_ns_vnf(group_id, element_id)
        # elif element_type == 'vnf_vl':
        #     result = projects[0].add_vnf_intvl(group_id, element_id)
        # elif element_type == 'vnf_ext_cp':
        #     result = projects[0].add_vnf_vnfextcpd(group_id, element_id)
        # elif element_type == 'vnf_vdu':
        #     result = projects[0].add_vnf_vdu(group_id, element_id)
        # elif element_type == 'vnf_vdu_cp':
        #     vdu_id = request.POST.get('choice')
        #     result = projects[0].add_vnf_vducp(group_id, vdu_id, element_id)
        # elif element_type == 'vnffg':
        #     print group_id, element_id
        #     result = projects[0].add_vnffg(group_id, element_id)

        status_code = 200 if result else 500
        response = HttpResponse(json.dumps({}), content_type="application/json", status=status_code)
        response["Access-Control-Allow-Origin"] = "*"
        return response


@login_required
def remove_element(request, project_id=None):
    if request.method == 'POST':
        #result = False
        # projects = EtsiProject.objects.filter(id=project_id)
        projects = Project.objects.filter(id=project_id).select_subclasses()
        result = projects[0].get_remove_element(request)

        # group_id = request.POST.get('group_id')
        # element_id = request.POST.get('element_id')
        # element_type = request.POST.get('element_type')
        # print 'in remove_element : ', element_id #TODO log
        # if element_type == 'ns_cp':
        #     result = projects[0].remove_ns_sap(group_id, element_id)
        # elif element_type == 'ns_vl':
        #     result = projects[0].remove_ns_vl(group_id, element_id)
        # elif element_type == 'vnf':
        #     result = projects[0].remove_ns_vnf(group_id, element_id)
        # elif element_type == 'vnf_vl':
        #     result = projects[0].remove_vnf_intvl(group_id, element_id)
        # elif element_type == 'vnf_ext_cp':
        #     result = projects[0].remove_vnf_vnfextcpd(group_id, element_id)
        # elif element_type == 'vnf_vdu':
        #     result = projects[0].remove_vnf_vdu(group_id, element_id)
        # elif element_type == 'vnf_vdu_cp':
        #     vdu_id = request.POST.get('choice')
        #     result = projects[0].remove_vnf_vducp(group_id, vdu_id, element_id)
        status_code = 200 if result else 500
        response = HttpResponse(json.dumps({}), content_type="application/json", status=status_code)
        response["Access-Control-Allow-Origin"] = "*"
        return response


@login_required
def add_link(request, project_id=None):
    if request.method == 'POST':
        # result = False
        # projects = EtsiProject.objects.filter(id=project_id)
        projects = Project.objects.filter(id=project_id).select_subclasses()
        result = projects[0].get_add_link(request)


        # source = json.loads(request.POST.get('source'))
        # destination = json.loads(request.POST.get('destination'))
        # source_type = source['info']['type']
        # destination_type = destination['info']['type']
        # if (source_type, destination_type) in [('ns_vl', 'ns_cp'), ('ns_cp', 'ns_vl')]:
        #     vl_id = source['id'] if source_type == 'ns_vl' else destination['id']
        #     sap_id = source['id'] if source_type == 'ns_cp' else destination['id']
        #     result = projects[0].link_vl_sap(source['info']['group'][0], vl_id, sap_id)
        # elif (source_type, destination_type) in [('ns_vl', 'vnf'), ('vnf', 'ns_vl')]:
        #     vl_id = source['id'] if source_type == 'ns_vl' else destination['id']
        #     vnf_id = source['id'] if source_type == 'vnf' else destination['id']
        #     ns_id = source['info']['group'][0]
        #     vnf_ext_cp = request.POST.get('choice')
        #     result = projects[0].link_vl_vnf(ns_id, vl_id, vnf_id, vnf_ext_cp)
        # if (source_type, destination_type) in [('vnf', 'ns_cp'), ('ns_cp', 'vnf')]:
        #     vnf_id = source['id'] if source_type == 'vnf' else destination['id']
        #     sap_id = source['id'] if source_type == 'ns_cp' else destination['id']
        #     ns_id = source['info']['group'][0]
        #     vnf_ext_cp = request.POST.get('choice')
        #     result = projects[0].link_vnf_sap(ns_id, vnf_id, sap_id, vnf_ext_cp)
        # elif (source_type, destination_type) in [('vnf_vl', 'vnf_vdu_cp'), ('vnf_vdu_cp', 'vnf_vl')]:
        #     vdu_id = request.POST.get('choice')
        #     vnf_id = source['info']['group'][0]
        #     intvl_id = source['id'] if source_type == 'vnf_vl' else destination['id']
        #     vducp_id = source['id'] if source_type == 'vnf_vdu_cp' else destination['id']
        #     result = projects[0].link_vducp_intvl(vnf_id, vdu_id, vducp_id, intvl_id)
        # elif (source_type, destination_type) in [('vnf_ext_cp', 'vnf_vl'), ('vnf_vl', 'vnf_ext_cp')]:
        #     vnfExtCpd_id = source['id'] if source_type == 'vnf_ext_cp' else destination['id']
        #     intvl_id = source['id'] if source_type == 'vnf_vl' else destination['id']
        #     result = projects[0].link_vnfextcpd_intvl(source['info']['group'][0], vnfExtCpd_id, intvl_id)
        status_code = 200 if result else 500
        response = HttpResponse(json.dumps({}), content_type="application/json", status=status_code)
        response["Access-Control-Allow-Origin"] = "*"
        return response


@login_required
def remove_link(request, project_id=None):
    if request.method == 'POST':
        # result = False
        # projects = EtsiProject.objects.filter(id=project_id)
        projects = Project.objects.filter(id=project_id).select_subclasses()
        result = projects[0].get_remove_link(request)

        # source = json.loads(request.POST.get('source'))
        # destination = json.loads(request.POST.get('destination'))
        # source_type = source['info']['type']
        # destination_type = destination['info']['type']
        # if (source_type, destination_type) in [('ns_vl', 'ns_cp'), ('ns_cp', 'ns_vl')]:
        #     vl_id = source['id'] if source_type == 'ns_vl' else destination['id']
        #     sap_id = source['id'] if source_type == 'ns_cp' else destination['id']
        #     result = projects[0].unlink_vl_sap(source['info']['group'][0], vl_id, sap_id)
        # elif (source_type, destination_type) in [('ns_vl', 'vnf'), ('vnf', 'ns_vl')]:
        #     vl_id = source['id'] if source_type == 'ns_vl' else destination['id']
        #     vnf_id = source['id'] if source_type == 'vnf' else destination['id']
        #     ns_id = source['info']['group'][0]
        #     result = projects[0].unlink_vl_vnf(ns_id, vl_id, vnf_id)
        # if (source_type, destination_type) in [('vnf', 'ns_cp'), ('ns_cp', 'vnf')]:
        #     vnf_id = source['id'] if source_type == 'vnf' else destination['id']
        #     sap_id = source['id'] if source_type == 'ns_cp' else destination['id']
        #     ns_id = source['info']['group'][0]
        #     result = projects[0].unlink_vl_sap(ns_id, vnf_id, sap_id)
        # elif (source_type, destination_type) in [('vnf_vl', 'vnf_vdu_cp'), ('vnf_vdu_cp', 'vnf_vl')]:
        #     print source, destination
        #     intvl_id = source['id'] if source_type == 'vnf_vl' else destination['id']
        #     vducp_id = source['id'] if source_type == 'vnf_vdu_cp' else destination['id']
        #     vnf_id = source['info']['group'][0]
        #     result = projects[0].unlink_vducp_intvl(vnf_id, vducp_id, intvl_id)
        # elif (source_type, destination_type) in [('vnf_ext_cp', 'vnf_vl'), ('vnf_vl', 'vnf_ext_cp')]:
        #     vnfExtCpd_id = source['id'] if source_type == 'vnf_ext_cp' else destination['id']
        #     intvl_id = source['id'] if source_type == 'vnf_vl' else destination['id']
        #     result = projects[0].unlink_vnfextcpd_intvl(source['info']['group'][0], vnfExtCpd_id, intvl_id)
        status_code = 200 if result else 500
        response = HttpResponse(json.dumps({}), content_type="application/json", status=status_code)
        response["Access-Control-Allow-Origin"] = "*"
        return response


@login_required
def add_node_to_vnffg(request, project_id=None):
    print "add_node_to_vnffg" #TODO log
    if request.method == 'POST':
        # projects = EtsiProject.objects.filter(id=project_id)
        projects = Project.objects.filter(id=project_id).select_subclasses()
        result = projects[0].add_node_to_vnffg(request)
        # group_id = request.POST.get('group_id')
        # element_id = request.POST.get('element_id')
        # element_type = request.POST.get('element_type')
        # vnffg_id = request.POST.get('vnffg_id')
        # print group_id, element_id, element_type, vnffg_id
        # result = projects[0].add_node_to_vnffg(group_id, vnffg_id, element_type, element_id)
    # status_code = 200 if result else 500
    # response = HttpResponse(json.dumps({}), content_type="application/json", status=status_code)
    # response["Access-Control-Allow-Origin"] = "*"
    # return response
        status_code = 200 if result else 500
        response = HttpResponse(json.dumps({}), content_type="application/json", status=status_code)
        response["Access-Control-Allow-Origin"] = "*"
        return response
