import json
import yaml
import os
import re
import logging
from unsortable_ordered_dict import UnsortableOrderedDict
from superfluidity_parser import SuperfluidityParser

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('AnsibleUtility.py')


class AnsibleUtility(object):

    def __init__(self):
        log.info("Constructor")
        pass

    def generate_playbook(self, sf_data, name, pb_path):
        try:
            # Temp vars
            host = "provider-master"
            # FIXME: Should be later updated to be taken
            # from the RDCL tool
            # (with the proper edge/core nodes names/ips)

            # Regex
            m = re.search('[a-z0-9]([-a-z0-9]*[a-z0-9])?', name.lower())

            application_name = m.group(0)

            nc_roles = self.create_roles(sf_data, application_name)
            roles = list(nc_roles)

            k8s_name = self.get_k8s_name(sf_data, nc_roles)
            print 'nc_roles', nc_roles
            ############################################
            # Create folder structure
            self.makedir_p(os.path.join(pb_path, 'group_vars'))
            self.makedir_p(os.path.join(pb_path, 'roles'))
            # Roles subfloders
            for role in nc_roles:
                self.makedir_p(os.path.join(pb_path, 'roles', role, 'tasks'))
                if '-create' not in role and '-destroy' not in role:
                    self.makedir_p(os.path.join(pb_path, 'roles', role, 'vars'))
                    self.makedir_p(os.path.join(pb_path, 'roles', role, 'files'))

            ###########################################
            # Various config files

            # Clean roles
            roles = [str(roles[x]) for x in range(len(roles))]

            deploy_roles = []
            undeploy_roles = []
            for role in roles:
                if '-destroy' in role:
                    undeploy_roles.append(role)
                else:
                    deploy_roles.append(role)

            # Deploy site file
            deploy_file = [UnsortableOrderedDict(
                [("hosts", host), ("become", True), ("become_method", "sudo"), ("vars_files", ["group_vars/all"]),
                 ("roles", deploy_roles)])]

            dstfile = open(pb_path + 'site_deploy.yaml', 'w')
            UnsortableOrderedDict.dump(deploy_file, dstfile)
            dstfile.close()

            # Undeploy site file
            undeploy_file = [UnsortableOrderedDict(
                [("hosts", host), ("become", True), ("become_method", "sudo"), ("vars_files", ["group_vars/all"]),
                 ("roles", undeploy_roles)])]

            dstfile = open(pb_path + 'site_undeploy.yaml', 'w')
            yaml.dump(undeploy_file, dstfile, default_flow_style=False, explicit_start=True)
            dstfile.close()


            ###########################################
            # Variables

            # Group vars
            all_file = {"application_name": str(application_name)}

            dstfile = open(pb_path + 'group_vars/all', 'w')
            yaml.dump(all_file, dstfile, default_style='"', default_flow_style=False, explicit_start=True)
            dstfile.close()

            # Role vars
            for role in nc_roles:
                if '-create' in role or '-destroy' in role:
                    continue
                else:
                    main_file = {"json_path": "/tmp/" + k8s_name[role] + ".json"}

                dstfile = open(pb_path + 'roles/' + role + '/vars/main.yaml', 'w')
                yaml.safe_dump(main_file, dstfile, default_flow_style=False, explicit_start=True)
                dstfile.close()
            #############################################
            # Tasks

            # Role tasks
            for role in nc_roles:
                if '-create' in role:
                    main_file = [UnsortableOrderedDict(
                        [("name", "Create " + str(name) + " project"),
                         ("command", "kubectl create namespace {{ application_name }}")])]
                elif '-destroy' in role:
                    main_file = [UnsortableOrderedDict([("name", "Destroy " + str(name) + " project"),
                                                        ("command", "kubectl delete {{ application_name }}")])]
                else:
                    main_file = [UnsortableOrderedDict([
                        ("name", "copy json template file"),
                        ("copy", UnsortableOrderedDict({
                            ("src", str(role) + '.json'),
                            ("dest", "{{ json_path }}")}))
                    ]), UnsortableOrderedDict(
                        [("name", "Deploy " + str(role.split('-')[0]) + ' ' + str(role.split('-')[1]) + " app"),
                         ("command", "kubectl create -f {{ json_path }}")])]

                dstfile = open(pb_path + 'roles/' + role + '/tasks/main.yaml', 'w')
                UnsortableOrderedDict.dump(main_file, dstfile)
                dstfile.close()
            ############################################
            # Templates
            for role in nc_roles:
                if '-create' not in role and '-destroy' not in role:
                    data = self.sf_kubernetes(sf_data, role)
                    dstfile = open(os.path.join(pb_path, 'roles', role, 'files', role + '.json'), 'w')
                    json.dump(data, dstfile)
                    dstfile.close()
        except Exception as e:
            print "Exception in generate_playbook"
            log.exception(e)

    @staticmethod
    def create_roles(sf_data, name):
        roles = [name + '-create', name + '-destroy']
        for vnfd in sf_data['vnfd']:
            vnf = sf_data['vnfd'][vnfd]
            # print vnf['vdu']
            vdu_list = vnf['vdu']
            for vdu in vdu_list:
                if 'vduNestedDesc' in vdu and vdu['vduNestedDesc'] is not None:
                    vdu_nested_desc_id = vdu['vduNestedDesc']
                    vdu_nested = SuperfluidityParser().get_nested_vdu_from_id(vdu_nested_desc_id, vnf)
                    if vdu_nested and vdu_nested['vduNestedDescriptorType'] == 'kubernetes':
                        roles.append(vnfd + '-' + vdu['vduId'])
        return roles

    @staticmethod
    def sf_kubernetes(sf_data, role):
        split_role = role.split('-')
        # print split_role
        vnfd = split_role[0]
        vdu_name = split_role[1]
        vnf = sf_data['vnfd'][vnfd]
        vdu_list = vnf['vdu']
        for vdu in vdu_list:
            if vdu['vduId'] == vdu_name:
                if 'vduNestedDesc' in vdu and vdu['vduNestedDesc'] is not None:
                    vdu_nested_desc_id = vdu['vduNestedDesc']
                    vdu_nested = SuperfluidityParser().get_nested_vdu_from_id(vdu_nested_desc_id, vnf)
                    k8s_name = str(vdu_nested['vduNestedDescriptor'])
                    data = sf_data['k8s'][k8s_name]
                    return data
        return None

    @staticmethod
    def get_k8s_name(sf_data, roles):
        k8s_name = {}
        for role in roles:
            if "-create" not in role and "-destroy" not in role:
                vnfd = role.split('-')[0]
                vdu_id = role.split('-')[1]
                vnf = sf_data["vnfd"][vnfd]
                vdu_list = vnf['vdu']
                for vdu in vdu_list:
                    if vdu['vduId'] == vdu_id:
                        if 'vduNestedDesc' in vdu and vdu['vduNestedDesc'] is not None:
                            vdu_nested_desc_id = vdu['vduNestedDesc']
                            vdu_nested = SuperfluidityParser().get_nested_vdu_from_id(vdu_nested_desc_id, vnf)
                            # k8s_name.push(role)
                            k8s_name[role] = vdu_nested['vduNestedDescriptor']
        return k8s_name

    @staticmethod
    def makedir_p(directory):
        """makedir_p(path)

        Works like mkdirs, except that check if the leaf exist.

        """
        if not os.path.isdir(directory):
            os.makedirs(directory)
