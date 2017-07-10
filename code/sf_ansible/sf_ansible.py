import json
import pyaml
import yaml

from lib.clickparser import click_parser
from lib.etsi.etsi_parser import EtsiParser
from lib.util import Util
from lib.parser import Parser
from unsortable_ordered_dict import UnsortableOrderedDict
import logging
import traceback
import glob
import os
import re

def import_k8s(dir_project):
    files = []
    for file_name in glob.glob(os.path.join(dir_project, '*.'+'yaml')):
        files.append(Util().openfile(file_name))
    for file_name in glob.glob(os.path.join(dir_project, '*.'+'json')):
        files.append(Util().openfile(file_name))
    project = {
        'kubernetes': {}
    }
    for file in files:
        #file_stream = open(file,'r')
        project['kubernetes'][ os.path.splitext(os.path.basename(str(file)))[0]] = yaml.load(file)
    return project

def importprojectdir(dir_project):
    """Imports all descriptor files under a given folder

    this method is specific for Superfluidity project type
    """

    project = {
        'nsd':{},

        'vnfd':{},

        'kubernetes':{},

        'positions': {}
    }
    nfv_path = dir_project+"/NFV/"
    etsi_project = EtsiParser.importprojectdir( nfv_path + '/JSON', 'json')
    #print etsi_project
    project['nsd'] = etsi_project['nsd']
    project['vnfd'] = etsi_project['vnfd']
    project['kubernetes'] = import_k8s(dir_project + '/K8S/')['kubernetes']


    for vertices_file in glob.glob(os.path.join(dir_project, '*.json')):
        if os.path.basename(vertices_file) == 'vertices.json':
            project['positions']['vertices'] = Util.loadjsonfile(vertices_file)

    #print project

    return project

def SF2Kubernetes(sf_data, role):
    split_role = role.split('-')
    #print split_role
    vnfd = split_role[0]
    vdu_name = split_role[1]
    vnf = sf_data['vnfd'][vnfd]
    vdu_list = vnf['vdu']
    for vdu in vdu_list:
        if vdu['name'] == vdu_name:
            k8s_name = vdu['vduNestedDesc']
            #print k8s_name
            data = sf_data['kubernetes'][k8s_name]
    return data

def create_roles(sf_data, name):
    roles=[]
    roles.append(name + '-create')
    roles.append(name + '-destroy')
    for vnfd in sf_data['vnfd']:
        vnf = sf_data['vnfd'][vnfd]
        #print vnf['vdu']
        vdu_list = vnf['vdu']
        for vdu in vdu_list:
            #print vdu
            if 'vduNestedDescType' in vdu:
                if vdu['vduNestedDescType'] == 'kubernetes':
                    roles.append(vnfd+'-'+vdu['name'])
    return roles

def get_k8s_name(sf_data, roles):
    k8s_name = {}
    for role in roles:
        if "-create" not in role and "-destroy" not in role:
            vnfd = role.split('-')[0]
            vdu_name = role.split('-')[1]
            vnf = sf_data["vnfd"][vnfd]
            vdu_list = vnf['vdu']
            for vdu in vdu_list:
                if vdu['name'] == vdu_name:
                    #k8s_name.push(role)
                    k8s_name[role] = vdu['vduNestedDesc']
    return k8s_name

def generate_playbook(sf_data, name, pb_path):
    ###########################################
    #Temp vars
    host = "provider-master"    # FIXME: Should be later updated to be taken \
                                # from the RDCL tool
                                # (with the proper edge/core nodes names/ips)

    # Regex
    m = re.search('[a-z0-9]([-a-z0-9]*[a-z0-9])?', name.lower())
    print(m.group(0))

    application_name = m.group(0)

    nc_roles = create_roles(sf_data, application_name)
    roles = list(nc_roles)
    #roles.append("common")
    k8s_name = get_k8s_name(sf_data, nc_roles)

    ############################################
    #Create folder structure
    if not os.path.exists(pb_path):
        os.makedirs(pb_path)
        os.makedirs(pb_path + 'group_vars/')
        os.makedirs(pb_path + 'roles/')
        #os.makedirs(pb_path + 'roles/common/tasks/')
    #Roles folders
        for role in nc_roles:
            os.makedirs(pb_path + 'roles/' + role + '/')
            os.makedirs(pb_path + 'roles/' + role + '/tasks/')
            if '-create' not in role and '-destroy' not in role:
                os.makedirs(pb_path + 'roles/' + role + '/vars/')
                os.makedirs(pb_path + 'roles/' + role + '/files/')

    ###########################################
    #Various config files

    #Clean roles
    roles = [str(roles[x]) for x in range(len(roles))]


    deploy_roles = []
    undeploy_roles = []
    for role in roles:
        if '-destroy' in role:
            undeploy_roles.append(role)
        else:
            deploy_roles.append(role)

    # Deploy site file
    deploy_file = UnsortableOrderedDict([("hosts", host), ("become", "yes"), ("become_method", "sudo"), ("vars_files", ["group_vars/all"]), ("roles", deploy_roles)])

    dstfile = open(pb_path + 'site_deploy.yaml', 'w')
    UnsortableOrderedDict.dump(deploy_file, dstfile)
    dstfile.close

    # Undeploy site file
    undeploy_file = UnsortableOrderedDict([("hosts", host), ("become", "yes"), ("become_method", "sudo"), ("vars_files", ["group_vars/all"]), ("roles", undeploy_roles)])

    dstfile = open(pb_path + 'site_undeploy.yaml', 'w')
    yaml.dump(undeploy_file, dstfile, default_flow_style=False, explicit_start=True)
    dstfile.close

    # #site
    # site_file = [[{"include": "site_deploy.yaml"}], {"include": "site_undeploy.yaml"}]
    #
    # print(site_file)
    #
    # dstfile = open(pb_path+'site.yaml', 'w')
    # yaml.dump(site_file, dstfile, default_flow_style=False, explicit_start=True)
    # dstfile.close

    ###########################################
    #Variables

    #Group vars
    all_file = {"application_name": str(application_name)}

    dstfile = open(pb_path+'group_vars/all', 'w')
    yaml.dump(all_file, dstfile, default_style='"', default_flow_style=False, explicit_start=True)
    dstfile.close()

    #Role vars
    for role in nc_roles:
        if '-create' in role or '-destroy' in role:
            continue
        else:
            main_file = {"json_path": "/tmp/"+k8s_name[role]+".json"}

        dstfile = open(pb_path+'roles/'+role+'/vars/main.yaml', 'w')
        yaml.safe_dump(main_file, dstfile, default_flow_style=False, explicit_start=True)
        dstfile.close
    #############################################
    #Tasks

    #Role tasks
    for role in nc_roles:
        if '-create' in role:
            main_file = [UnsortableOrderedDict([("name", "Create " + str(name) + " project"), ("command", "oc new-project {{ application_name }}")])]
        elif '-destroy' in role:
            main_file = [UnsortableOrderedDict([("name", "Destroy " + str(name) + " project"), ("command", "oc delete project {{ application_name }}")])]
        else:
            main_file = [UnsortableOrderedDict([("name", "copy json template file"), ("copy", UnsortableOrderedDict([("src", str(role)+'.json'), ("dest", "{{ json_path }}")]))])]
            main_file.append(UnsortableOrderedDict([("name", "Deploy " + str(role.split('-')[0]) + ' ' + str(role.split('-')[1]) + " app"), ("command", "oc create -f {{ json_path }}")]))

        dstfile = open(pb_path+'roles/'+role+'/tasks/main.yaml', 'w')
        UnsortableOrderedDict.dump(main_file, dstfile)
        dstfile.close
    ############################################
    #Templates
    for role in nc_roles:
        if '-create' not in role and '-destroy' not in role:
            data=SF2Kubernetes(sf_data, role)
            dstfile = open(pb_path+'roles/'+role+'/files/'+role+'.json', 'w')
            json.dump(data, dstfile)
            dstfile.close()

###################################################################
#Here begins the testing
project_dir = 'examples/Superfluidity-example-k8s-01'
project = importprojectdir(project_dir)

for name in project['nsd']:
    pass
pb_path = 'playbooks/'+name.lower()+'/'
generate_playbook(project, name, pb_path)
