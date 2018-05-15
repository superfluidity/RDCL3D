import json
import yaml
import os
import re
import logging
import shutil

from lib.superfluidity.superfluidity_parser import SuperfluidityParser


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('AnsibleUtility.py')


def _load_data_from_file(file_object):
    try:
        json_object = json.load(file_object)
        return json_object
    except Exception as e:
        log.exception('Exception loadJsonFile', e)
        raise


class AnsibleUtility(object):
    def __init__(self):
        log.info("Constructor")
        pass

    def generate_playbook(self, sf_data, name, pb_path):
        try:
            self.BASE = pb_path
            self.roles_create = []
            self.roles_destroy = []
            # GENERATE A COMPLIANT APPLICATION NAME (non va bene)
            #m = re.search('[a-z0-9]([-a-z0-9]*[a-z0-9])?', name.lower())
            application_name = name.lower() # m.group(0)

            self.init_dir(os.path.join(self.BASE, 'group_vars'))
            self.init_group_vars_file('all', {'application_name': str(application_name).replace("_", "-")})

            self.init_dir(os.path.join(self.BASE, 'roles'))

            # APP CREATE ROLE
            self.init_dir(os.path.join(self.BASE, 'roles', str(application_name + '_create')))
            self.add_role_task(str(application_name + '_create'), 'main', [{'name': 'Create project',
                                                                       'command': 'kubectl create namespace {{ application_name }}'}])

            self.roles_create.append(str(application_name + '_create'))

            # APP DESTROY ROLE
            self.init_dir(os.path.join(self.BASE, 'roles', str(application_name + '_destroy')))
            self.add_role_task(str(application_name + '_destroy'), 'main', [{'name': 'Destroy project',
                                                                        'command': 'kubectl delete namespace {{ application_name }}'}])
            self.roles_destroy.append(str(application_name + '_destroy'))
            roles_create_order = []
            for v in sf_data['vnfd']:
                vnfd = sf_data['vnfd'][v]
                for vdu in vnfd['vdu']:
                    if 'vduNestedDesc' in vdu and vdu['vduNestedDesc'] is not None:
                        vdu_nested_desc_id = vdu['vduNestedDesc']
                        vdu_nested = SuperfluidityParser().get_nested_vdu_from_id(vdu_nested_desc_id, vnfd)
                        if vdu_nested and vdu_nested['vduNestedDescriptorType'] == 'kubernetes':
                            role_vars = {}
                            role_name = vdu['vduId']
                            k8s_name = str(vdu_nested['vduNestedDescriptor'])
                            data = sf_data['k8s'][k8s_name]
                            log.info("Generate role %s", role_name)
                            self.add_role_template(role_name, k8s_name, data)
                            role_vars['template_path_' + k8s_name] = '/tmp/' + k8s_name + '.yml'
                            main_tasks = []
                            podDependecies = self._get_properties_from_metadata(role_name, 'podDependencies', vnfd)
                            for dep in podDependecies:
                                for pod in podDependecies[dep]:
                                    main_tasks.append(self.get_commands_k8s_pod_property(dep, pod))
                            #k8s_pod_property
                            pause_sec = self._get_properties_from_metadata(role_name, 'deploymentPause', vnfd)
                            if pause_sec and isinstance(pause_sec, int):
                                main_tasks.append(self.get_commands_pause(pause_sec))

                            main_tasks.append({'name': 'Create the json file from template', 'template': {'dest': '{{template_path_' + k8s_name + '}}',
                                                                                            'src': k8s_name + '.yml'}})
                            main_tasks.append({'name': 'Deploy ' + k8s_name,
                                 'command': 'kubectl create -f {{template_path_' + k8s_name + '}} --namespace={{application_name}}'
                                 })

                            self.add_role_task(role_name, 'main', main_tasks)

                            self.add_role_var(role_name, 'main', role_vars)
                            deployment_order = self._get_properties_from_metadata(role_name, 'deploymentOrder', vnfd)
                            if deployment_order and isinstance(deployment_order, int):
                                roles_create_order.append((deployment_order, str(role_name)))
                            print ("Depl order: ", deployment_order)
                            #self.roles_create.append(str(role_name))
            print roles_create_order
            roles_create_order_sorted = sorted(roles_create_order, key=lambda x: x[0])
            roles_create_order = [r[1] for r in roles_create_order_sorted]
            self.roles_create = self.roles_create + roles_create_order

            self.add_playbook_file('site_app_create', [{'hosts': 'provider-master', 'vars_files': ['group_vars/all'], 'roles': self.roles_create,
                                                       'become': 'yes', 'become_user': 'bilal', 'become_method': 'su'}])
            self.add_playbook_file('site_app_destroy', [{'hosts': 'provider-master', 'vars_files': ['group_vars/all'], 'roles': self.roles_destroy}])

        except Exception as e:
            print "Exception in generate_playbook"
            log.exception(e)

    def get_commands_pause(self, sec):
        return {'name': "Pause",
                'pause': {"seconds": sec}
                }
    def get_commands_k8s_pod_property(self, property, pod_name):
        if property == 'podIP':
            return {'name': "Getting {0} from {1}".format(property, pod_name),
                    'command': str("kubectl get pods -o jsonpath='{.items[?(@.metadata.labels.name==\""+pod_name+"\")].status.podIP}' --namespace={{ application_name }}"),
                    'register': str(pod_name+ '_ip')
                    }

    def init_dir(self, dir_path):
        log.info("init_dir " + dir_path)
        shutil.rmtree(dir_path, ignore_errors=True)
        self.makedir_p(dir_path)

    def init_group_vars_file(self, group_name, vars_data):
        log.info('Init a variables file for "%s" group', group_name)
        group_var_path = os.path.join(self.BASE, 'group_vars', group_name)
        yaml.dump(vars_data, open(group_var_path, 'w'), default_flow_style=False, explicit_start=True,
                  width=float("inf"))


    def add_role_task(self, role_name, task_name, task_data):
        log.info('Add %s task to %s role', task_name, role_name)
        tasks_path = os.path.join(self.BASE, 'roles', role_name, 'tasks')
        task_path = os.path.join(tasks_path, task_name + '.yaml')
        self.makedir_p(tasks_path)
        yaml.dump(task_data, open(task_path, 'w'), default_flow_style=False, explicit_start=True,
                  width=float("inf"))

    def add_role_var(self, role_name, vars_name, var_data):
        log.info('Add %s vars to %s role', vars_name, role_name)
        vars_path = os.path.join(self.BASE, 'roles', role_name, 'vars')
        var_path = os.path.join(vars_path, vars_name + '.yaml')
        self.makedir_p(vars_path)
        yaml.dump(var_data, open(var_path, 'w'), default_flow_style=False, explicit_start=True,
                  width=float("inf"))

    def add_role_template(self, role_name, template_name, template_data):
        log.info('Add %s template to %s role', template_name, role_name)
        templates_path = os.path.join(self.BASE, 'roles', role_name, 'templates')
        template_path = os.path.join(templates_path, template_name + '.yml')
        self.makedir_p(templates_path)
        yaml.safe_dump(yaml.load(json.dumps(template_data)), open(template_path, 'w'), default_flow_style=False,
                       width=float("inf"))

    def add_playbook_file(self, name, playbook_data):
        log.info('Add %s playbook file', name)
        playbook_path = os.path.join(self.BASE, name + '.yaml')
        yaml.dump(playbook_data, open(playbook_path, 'w'), default_flow_style=False, explicit_start=True,
                  width=float("inf"))

    @staticmethod
    def _get_properties_from_metadata(element_id, meta_name, vnf_data):
        metadata_list = vnf_data['modifiableAttributes']['metadata']
        for metadata in metadata_list:
            if meta_name in metadata:
                for prop in metadata[meta_name]:
                    if element_id in prop:
                        if isinstance(prop[element_id], list):
                            meta_prop = dict(pair for d in prop[element_id] for pair in d.items())
                            return meta_prop
                        else:
                            return prop[element_id]
        return {}

    @staticmethod
    def makedir_p(directory):
        """makedir_p(path)

        Works like mkdirs, except that check if the leaf exist.

        """
        if not os.path.isdir(directory):
            os.makedirs(directory)




# if __name__ == '__main__':
#     a_test = AnsibleUtility()
#     input_data = _load_data_from_file(open('nsd_test.json', 'r', 1))
#     playbook_output_dir = 'nsd_test'
#     # print input_data
#     a_test.generate_playbook(input_data, 'nsdtest', playbook_output_dir)
