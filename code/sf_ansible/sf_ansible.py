import json
import yaml


from lib.etsi.etsi_parser import EtsiParser
from lib.util import Util
from unsortable_ordered_dict import UnsortableOrderedDict
import glob
import os

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
    split_role = role.split('_')
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
    roles.append(name + '_create')
    roles.append(name + '_destroy')
    for vnfd in sf_data['vnfd']:
        vnf = sf_data['vnfd'][vnfd]
        #print vnf['vdu']
        vdu_list = vnf['vdu']
        for vdu in vdu_list:
            #print vdu
            if 'vduNestedDescType' in vdu:
                if vdu['vduNestedDescType'] == 'kubernetes':
                    roles.append(vnfd+'_'+vdu['name'])
    return roles

def get_k8s_name(sf_data, roles):
    k8s_name = {}
    for role in roles:
        if "_create" not in role and "_destroy" not in role:
            vnfd = role.split('_')[0]
            vdu_name = role.split('_')[1]
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
    host = "openshift_master"

    openshift_master_url= "localhost"
    openshift_master_port = "8443"
    openshift_admin_username = "admin"
    openshift_admin_password = "admin"
    application_name = name

    nc_roles = create_roles(sf_data, name)
    roles = list(nc_roles)
    roles.append("common")
    k8s_name = get_k8s_name(sf_data, nc_roles)

    ############################################
    #Create folder structure
    if not os.path.exists(pb_path):
        os.makedirs(pb_path)
        os.makedirs(pb_path + 'group_vars/')
        os.makedirs(pb_path + 'roles/')
        os.makedirs(pb_path + 'roles/common/tasks/')
    #Roles folders
        for role in nc_roles:
            os.makedirs(pb_path + 'roles/' + role + '/')
            os.makedirs(pb_path + 'roles/' + role + '/vars/')
            os.makedirs(pb_path + 'roles/' + role + '/tasks/')
            if '_create' not in role and '_destroy' not in role:
                os.makedirs(pb_path + 'roles/' + role + '/templates/')

    ###########################################
    #Various config files

    #ansible.cfg
    dstfile = open(pb_path+'ansible.cfg', 'w')

    dstfile.write("[defaults]\n")
    dstfile.write("host_key_checking = False\n")
    dstfile.write("forks = 500\n")
    dstfile.write("pipelining = True\n")
    dstfile.write("timeout = 30\n")
    dstfile.write("inventory = ./hosts\n")
    dstfile.write("retry_files_enabled = False")

    dstfile.close()

    #site
    site_file = [{"hosts": host, "become": "yes", "become_method": "sudo", "vars_files": ["group_vars/all"], "roles": roles}]

    dstfile = open(pb_path+'site.yaml', 'w')
    yaml.dump(site_file, dstfile, default_flow_style=False, explicit_start=True)
    dstfile.close

    ###########################################
    #Variables

    #Group vars
    all_file = {"openshift_master_url": openshift_master_url, "openshift_master_port": openshift_master_port, "openshift_admin_username": openshift_admin_username, "openshift_admin_password": openshift_admin_password, "application_name": application_name}

    dstfile = open(pb_path+'group_vars/all', 'w')
    yaml.dump(all_file, dstfile, default_style='"', default_flow_style=False, explicit_start=True)
    dstfile.close()

    #Role vars
    for role in nc_roles:
        if '_create' in role:
            main_file = {"post_args": ""}
        elif '_destroy' in role:
            main_file = {"post_args": ""}
        else:
            main_file = {"post_args": "", "json_path": "/tmp/"+k8s_name[role]+".json"}

        dstfile = open(pb_path+'roles/'+role+'/vars/main.yaml', 'w')
        yaml.safe_dump(main_file, dstfile, default_flow_style=False, explicit_start=True)
        dstfile.close
    #############################################
    #Tasks

    #Common tasks
    cmd ="oc login {{ openshift_master_url }}:{{ openshift_master_port }} -u{{ openshift_admin_username }} -p{{ openshift_admin_password }} --insecure-skip-tls-verify"
    main_file = [UnsortableOrderedDict([("name", "oc login"), ("command", cmd)])]
    dstfile = open(pb_path+'roles/common/tasks/main.yaml', 'w')
    UnsortableOrderedDict.dump(main_file, dstfile)
    dstfile.close

    #Role tasks
    for role in nc_roles:
        if '_create' in role:
            main_file = [UnsortableOrderedDict([("name", "Create " + str(name) + " project"), ("command", "oc new-project {{ application_name }}")])]
        elif '_destroy' in role:
            main_file = [UnsortableOrderedDict([("name", "Destroy " + str(name) + " project"), ("command", "oc delete project {{ application_name }}")])]
        else:
            main_file = [{"name": "Fetch json template", "template": UnsortableOrderedDict([("src", str(role)+'.json'), ("dest", "\"{{ json_path }}\"")])}]
            main_file.append(UnsortableOrderedDict([("name", "Deploy " + str(role.split('_')[0]) + ' ' + str(role.split('_')[1]) + " app"), ("command", "oc create -f {{ json_path }} {{ post_args }}")]))

        dstfile = open(pb_path+'roles/'+role+'/tasks/main.yaml', 'w')
        UnsortableOrderedDict.dump(main_file, dstfile)
        dstfile.close
    ############################################
    #Templates
    for role in nc_roles:
        if '_create' not in role and '_destroy' not in role:
            data=SF2Kubernetes(sf_data, role)
            dstfile = open(pb_path+'roles/'+role+'/templates/'+role+'.json', 'w')
            json.dump(data, dstfile)
            dstfile.close()

###################################################################
#Here begins the testing
project_dir = 'examples/Superfluidity-example-k8s-01'
project = importprojectdir(project_dir)

for name in project['nsd']:
    pass
pb_path = 'playbooks/'+name+'/'
generate_playbook(project, name, pb_path)
