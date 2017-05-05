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

from __future__ import unicode_literals

import copy
import json
import os.path
import yaml
from lib.etsi.etsi_parser import EtsiParser
from lib.etsi.etsi_rdcl_graph import EtsiRdclGraph
from lib.util import Util
from projecthandler.models import Project
import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('EtsiModel.py')

# project_types['etsi']= projecthandler.etsi_model.EtsiProject
# project_types['click']= ClickProject

PATH_TO_SCHEMAS = 'lib/etsi/schemas/'
PATH_TO_DESCRIPTORS_TEMPLATES = 'lib/etsi/descriptor_template'
DESCRIPTOR_TEMPLATE_SUFFIX = '.json'
GRAPH_MODEL_FULL_NAME = 'lib/TopologyModels/etsi/etsi.yaml'
EXAMPLES_FOLDER = 'usecases/ETSI/'


class EtsiProject(Project):
    """Etsi Project class
    The data model has the following descriptors:
    'nsd'
    'vnfd'
    'vnffgd'
    'vld'
    """

    @classmethod
    def data_project_from_files(cls, request):

        file_dict = {}
        for my_key in request.FILES.keys():
            file_dict[my_key] = request.FILES.getlist(my_key)

        log.info(file_dict)

        data_project = EtsiParser.importprojectfiles(file_dict)

        return data_project

    @classmethod
    def data_project_from_example(cls, request):
        example_id = request.POST.get('example-etsi-id', '')
        data_project = EtsiParser.importprojectdir(EXAMPLES_FOLDER + example_id + '/JSON', 'json')
        return data_project

    @classmethod
    def get_example_list(cls):
        """Returns a list of directories, in each directory there is a project example"""

        path = EXAMPLES_FOLDER
        dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
        return {'etsi': dirs}

    @classmethod
    def get_json_schema_by_type(cls, type_descriptor):
        schema = PATH_TO_SCHEMAS + type_descriptor + ".json"
        return schema

    @classmethod
    def get_new_descriptor(cls, descriptor_type, request_id):

        json_template = cls.get_descriptor_template(descriptor_type)
        if descriptor_type == 'nsd':
            json_template['nsdIdentifier'] = request_id
            json_template['nsdInvariantId'] = request_id
        else:
            json_template['vnfdId'] = request_id

        return json_template

    @classmethod
    def get_descriptor_template(cls, type_descriptor):
        """Returns a descriptor template for a given descriptor type"""

        try:
            schema = Util.loadjsonfile(os.path.join(PATH_TO_DESCRIPTORS_TEMPLATES, type_descriptor + DESCRIPTOR_TEMPLATE_SUFFIX))
            # print 'type_descriptor : '+type_descriptor
            return schema
        except Exception as e:
            log.exception(e)
            return False

    @classmethod
    def get_clone_descriptor(cls, descriptor, type_descriptor, new_descriptor_id):
        new_descriptor = copy.deepcopy(descriptor)
        if type_descriptor == 'vnfd':
            new_extention = "_" + new_descriptor_id
            new_descriptor['vnfdId'] = new_descriptor_id;
            new_descriptor['vnfProductName'] = new_descriptor['vnfProductName'] + new_extention if new_descriptor[
                                                                                                       'vnfProductName'] is not None else \
                new_descriptor['vnfProductName']
            for vnfExtCpd in new_descriptor['vnfExtCpd']:
                vnfExtCpd['cpdId'] = vnfExtCpd['cpdId'] + new_extention if vnfExtCpd['cpdId'] is not None else \
                    vnfExtCpd['cpdId']
        if type_descriptor == 'nsd':
            new_extention = "_" + new_descriptor_id
            new_descriptor['nsdIdentifier'] = new_descriptor_id
            new_descriptor['nsdName'] = new_descriptor_id
            new_descriptor['nsdInvariantId'] = new_descriptor_id
            for sapd in new_descriptor['sapd']:
                sapd['cpdId'] = sapd['cpdId'] + new_extention if sapd['cpdId'] is not None else sapd['cpdId']
        return new_descriptor

    def get_type(self):
        return "etsi"

    def __str__(self):
        return self.name

    def get_overview_data(self):
        current_data = json.loads(self.data_project)
        result = {
            'owner': self.owner.__str__(),
            'name': self.name,
            'updated_date': self.updated_date.__str__(),
            'info': self.info,
            'type': 'etsi',
            'nsd': len(current_data['nsd'].keys()) if 'nsd' in current_data else 0,
            'vnfd': len(current_data['vnfd'].keys()) if 'vnfd' in current_data else 0,
            'validated': self.validated
        }

        return result

    def get_graph_data_json_topology(self, descriptor_id):
        test_t3d = EtsiRdclGraph()
        project = self.get_dataproject()
        ##FIXME da rivedere, credo sia necessario rivedere questo processo
        topology = test_t3d.build_graph_from_project(project,
                                                     model=self.get_graph_model(GRAPH_MODEL_FULL_NAME))

        return json.dumps(topology)

    def create_descriptor(self, descriptor_name, type_descriptor, new_data, data_type):
        """Creates a descriptor of a given type from a json or yaml representation

        Returns the descriptor id or False
        """
        try:
            # utility = Util()
            current_data = json.loads(self.data_project)
            if data_type == 'json':
                new_descriptor = json.loads(new_data)
            elif data_type == 'yaml':
                # utility = Util()
                yaml_object = yaml.load(new_data)
                new_descriptor = json.loads(Util.yaml2json(yaml_object))
            else:
                log.debug('Create descriptor: Unknown data type')
                return False

            # schema = cls.loadjsonfile("lib/etsi/schemas/"+type_descriptor+".json")
            reference_schema = self.get_json_schema_by_type(type_descriptor)
            # validate = Util.validate_json_schema(reference_schema, new_descriptor)
            validate = False
            new_descriptor_id = new_descriptor['vnfdId'] if type_descriptor != "nsd" else new_descriptor[
                'nsdIdentifier']
            if not type_descriptor in current_data:
                current_data[type_descriptor] = {}
            current_data[type_descriptor][new_descriptor_id] = new_descriptor
            self.data_project = current_data
            self.validated = validate  # TODO(stefano) not clear if this is the validation for the whole project
            self.update()
            result = new_descriptor_id
        except Exception as e:
            log.exception(e)
            result = False
        return result

    def set_validated(self, value):
        self.validated = True if value is not None and value == True else False

    def get_add_element(self, request):

        result = False
        group_id = request.POST.get('group_id')
        element_id = request.POST.get('element_id')
        element_type = request.POST.get('element_type')
        existing_vnf = request.POST.get('existing_vnf')
        if element_type == 'ns_cp':
            result = self.add_ns_sap(group_id, element_id)
        elif element_type == 'ns_vl':
            result = self.add_ns_vl(group_id, element_id)
        elif element_type == 'vnf':
            if existing_vnf == 'true':
                result = self.add_ns_existing_vnf(group_id, element_id)
            else:
                result = self.add_ns_vnf(group_id, element_id)
        elif element_type == 'vnf_vl':
            result = self.add_vnf_intvl(group_id, element_id)
        elif element_type == 'vnf_ext_cp':
            result = self.add_vnf_vnfextcpd(group_id, element_id)
        elif element_type == 'vnf_vdu':
            result = self.add_vnf_vdu(group_id, element_id)
        elif element_type == 'vnf_vdu_cp':
            vdu_id = request.POST.get('choice')
            result = self.add_vnf_vducp(group_id, vdu_id, element_id)
        elif element_type == 'vnffg':
            # log.debug("Add ") group_id, element_id
            result = self.add_vnffg(group_id, element_id)

        return result

    def get_remove_element(self, request):

        result = False
        group_id = request.POST.get('group_id')
        element_id = request.POST.get('element_id')
        element_type = request.POST.get('element_type')
        log.debug('in get_remove_element : ' + str(element_id))  # TODO log
        if element_type == 'ns_cp':
            result = self.remove_ns_sap(group_id, element_id)
        elif element_type == 'ns_vl':
            result = self.remove_ns_vl(group_id, element_id)
        elif element_type == 'vnf':
            result = self.remove_ns_vnf(group_id, element_id)
        elif element_type == 'vnf_vl':
            result = self.remove_vnf_intvl(group_id, element_id)
        elif element_type == 'vnf_ext_cp':
            result = self.remove_vnf_vnfextcpd(group_id, element_id)
        elif element_type == 'vnf_vdu':
            result = self.remove_vnf_vdu(group_id, element_id)
        elif element_type == 'vnf_vdu_cp':
            vdu_id = request.POST.get('choice')
            result = self.remove_vnf_vducp(group_id, vdu_id, element_id)

        return result

    def get_add_link(self, request):

        result = False
        parameters = request.POST.dict()
        link = json.loads(parameters['link'])
        source = link['source']
        destination = link['target']
        #source = json.loads(request.POST.get('source'))
        #destination = json.loads(request.POST.get('destination'))
        source_type = source['info']['type']
        destination_type = destination['info']['type']
        if (source_type, destination_type) in [('ns_vl', 'ns_cp'), ('ns_cp', 'ns_vl')]:
            vl_id = source['id'] if source_type == 'ns_vl' else destination['id']
            sap_id = source['id'] if source_type == 'ns_cp' else destination['id']
            result = self.link_vl_sap(source['info']['group'][0], vl_id, sap_id)
        elif (source_type, destination_type) in [('ns_vl', 'vnf'), ('vnf', 'ns_vl')]:
            vl_id = source['id'] if source_type == 'ns_vl' else destination['id']
            vnf_id = source['id'] if source_type == 'vnf' else destination['id']
            ns_id = source['info']['group'][0]
            vnf_ext_cp = request.POST.get('choice')
            result = self.link_vl_vnf(ns_id, vl_id, vnf_id, vnf_ext_cp)
        if (source_type, destination_type) in [('vnf', 'ns_cp'), ('ns_cp', 'vnf')]:
            vnf_id = source['id'] if source_type == 'vnf' else destination['id']
            sap_id = source['id'] if source_type == 'ns_cp' else destination['id']
            ns_id = source['info']['group'][0]
            vnf_ext_cp = request.POST.get('choice')
            result = self.link_vnf_sap(ns_id, vnf_id, sap_id, vnf_ext_cp)
        elif (source_type, destination_type) in [('vnf_vl', 'vnf_vdu_cp'), ('vnf_vdu_cp', 'vnf_vl')]:
            vdu_id = request.POST.get('choice')
            vnf_id = source['info']['group'][0]
            intvl_id = source['id'] if source_type == 'vnf_vl' else destination['id']
            vducp_id = source['id'] if source_type == 'vnf_vdu_cp' else destination['id']
            result = self.link_vducp_intvl(vnf_id, vdu_id, vducp_id, intvl_id)
        elif (source_type, destination_type) in [('vnf_ext_cp', 'vnf_vl'), ('vnf_vl', 'vnf_ext_cp')]:
            vnfExtCpd_id = source['id'] if source_type == 'vnf_ext_cp' else destination['id']
            intvl_id = source['id'] if source_type == 'vnf_vl' else destination['id']
            result = self.link_vnfextcpd_intvl(source['info']['group'][0], vnfExtCpd_id, intvl_id)
        return result

    def get_remove_link(self, request):

        result = False
        parameters = request.POST.dict()
        #print "param remove_link", parameters
        link = json.loads(parameters['link'])
        source = link['source']
        destination = link['target']

        source_type = source['info']['type']
        destination_type = destination['info']['type']
        if (source_type, destination_type) in [('ns_vl', 'ns_cp'), ('ns_cp', 'ns_vl')]:
            vl_id = source['id'] if source_type == 'ns_vl' else destination['id']
            sap_id = source['id'] if source_type == 'ns_cp' else destination['id']
            result = self.unlink_vl_sap(source['info']['group'][0], vl_id, sap_id)
        elif (source_type, destination_type) in [('ns_vl', 'vnf'), ('vnf', 'ns_vl')]:
            vl_id = source['id'] if source_type == 'ns_vl' else destination['id']
            vnf_id = source['id'] if source_type == 'vnf' else destination['id']
            ns_id = source['info']['group'][0]
            result = self.unlink_vl_vnf(ns_id, vl_id, vnf_id)
        if (source_type, destination_type) in [('vnf', 'ns_cp'), ('ns_cp', 'vnf')]:
            vnf_id = source['id'] if source_type == 'vnf' else destination['id']
            sap_id = source['id'] if source_type == 'ns_cp' else destination['id']
            ns_id = source['info']['group'][0]
            result = self.unlink_vl_sap(ns_id, vnf_id, sap_id)
        elif (source_type, destination_type) in [('vnf_vl', 'vnf_vdu_cp'), ('vnf_vdu_cp', 'vnf_vl')]:
            intvl_id = source['id'] if source_type == 'vnf_vl' else destination['id']
            vducp_id = source['id'] if source_type == 'vnf_vdu_cp' else destination['id']
            vnf_id = source['info']['group'][0]
            result = self.unlink_vducp_intvl(vnf_id, vducp_id, intvl_id)
        elif (source_type, destination_type) in [('vnf_ext_cp', 'vnf_vl'), ('vnf_vl', 'vnf_ext_cp')]:
            vnfExtCpd_id = source['id'] if source_type == 'vnf_ext_cp' else destination['id']
            intvl_id = source['id'] if source_type == 'vnf_vl' else destination['id']
            result = self.unlink_vnfextcpd_intvl(source['info']['group'][0], vnfExtCpd_id, intvl_id)
        return result

    def get_unused_vnf(self, nsd_id):
        try:
            current_data = json.loads(self.data_project)
            result = []
            if 'vnfd' in current_data:
                for vnf in current_data['vnfd']:
                    if vnf not in current_data['nsd'][nsd_id]['vnfdId']:
                        result.append(vnf)
        except Exception as e:
            log.exception(e)
            result = None  # TODO maybe we should use False ?
        return result

    def get_available_nodes(self, args):
        """Returns all available node """
        log.debug('get_available_nodes')
        try:
            result = []
            #current_data = json.loads(self.data_project)
            model_graph = self.get_graph_model(GRAPH_MODEL_FULL_NAME)
            for node in model_graph['layer'][args['layer']]['nodes']:
                if 'addable' in model_graph['layer'][args['layer']]['nodes'][node] and model_graph['layer'][args['layer']]['nodes'][node]['addable']:
                    current_data = {
                        "id": node,
                        "category_name": model_graph['nodes'][node]['label'],
                        "types": [
                            {
                                "name": "generic",
                                "id": node
                            }
                        ]
                    }
                    result.append(current_data)

            #result = current_data[type_descriptor][descriptor_id]
        except Exception as e:
            log.debug(e)
            result = []
        return result

    # NS operations: add/remove VL
    def add_ns_vl(self, ns_id, vl_id):
        try:
            current_data = json.loads(self.data_project)
            ns = self.get_descriptor_template('nsd')
            vl_descriptor = ns['virtualLinkDesc'][0]
            vl_descriptor['virtualLinkDescId'] = vl_id
            current_data['nsd'][ns_id]['virtualLinkDesc'].append(vl_descriptor)
            virtualLinkProfile = ns['nsDf'][0]['virtualLinkProfile'][0]
            virtualLinkProfile['virtualLinkProfileId'] = "virtualLinkProfileId" + vl_id
            virtualLinkProfile['virtualLinkDescId'] = vl_id
            current_data['nsd'][ns_id]['nsDf'][0]['virtualLinkProfile'].append(virtualLinkProfile)
            self.data_project = current_data
            self.update()
            result = True
        except Exception as e:
            log.exception(e)
            result = False
        return result

    def remove_ns_vl(self, ns_id, vl_id):
        try:
            current_data = json.loads(self.data_project)
            vl_descriptor = next(
                (x for x in current_data['nsd'][ns_id]['virtualLinkDesc'] if x['virtualLinkDescId'] == vl_id), None)
            if vl_descriptor is not None:
                current_data['nsd'][ns_id]['virtualLinkDesc'].remove(vl_descriptor)
            vl_profile = next((x for x in current_data['nsd'][ns_id]['nsDf'][0]['virtualLinkProfile'] if
                               x['virtualLinkDescId'] == vl_id), None)
            if vl_profile is not None:
                vl_profile_id = vl_profile['virtualLinkProfileId']
                current_data['nsd'][ns_id]['nsDf'][0]['virtualLinkProfile'].remove(vl_profile)
                for nsDf in current_data['nsd'][ns_id]['nsDf']:
                    for vnfProfile in nsDf["vnfProfile"]:
                        for nsVirtualLinkConnectivity in vnfProfile['nsVirtualLinkConnectivity']:
                            if nsVirtualLinkConnectivity['virtualLinkProfileId'] == vl_profile_id:
                                vnfProfile['nsVirtualLinkConnectivity'].remove(nsVirtualLinkConnectivity)
            for sapd in current_data['nsd'][ns_id]['sapd']:
                if 'nsVirtualLinkDescId' in sapd and sapd['nsVirtualLinkDescId'] == vl_id:
                    sapd['nsVirtualLinkDescId'] = None
            self.data_project = current_data
            self.update()
            result = True
        except Exception as e:
            log.exception(e)
            result = False
        return result

    def edit_ns_vl(self, ns_id, vl_id, vl_descriptor):
        try:
            current_data = json.loads(self.data_project)
            self.remove_ns_vl(ns_id, vl_id)
            current_data['nsd'][ns_id]['virtualLinkDesc'].append(vl_descriptor)
            self.data_project = current_data
            self.update()
            result = True
        except Exception as e:
            log.exception(e)
            result = False
        return result

    # NS operations: add/remove SAP
    def add_ns_sap(self, ns_id, sap_id):
        try:
            current_data = json.loads(self.data_project)
            # utility = Util()
            ns = self.get_descriptor_template('nsd')
            sap_descriptor = ns['sapd'][0]
            sap_descriptor['cpdId'] = sap_id
            current_data['nsd'][ns_id]['sapd'].append(sap_descriptor)
            self.data_project = current_data
            self.update()
            result = True
        except Exception as e:
            log.exception(e)
            result = False
        return result

    def remove_ns_sap(self, ns_id, sap_id):
        try:
            current_data = json.loads(self.data_project)
            sap_descriptor = next((x for x in current_data['nsd'][ns_id]['sapd'] if x['cpdId'] == sap_id), None)
            if sap_descriptor is not None:
                current_data['nsd'][ns_id]['sapd'].remove(sap_descriptor)
            self.data_project = current_data
            self.update()
            result = True
        except Exception as e:
            log.exception(e)
            result = False
        return result

    def edit_ns_sap(self, ns_id, sap_id, sap_descriptor):
        try:
            current_data = json.loads(self.data_project)
            self.remove_ns_sap(ns_id, sap_id)
            current_data['nsd'][ns_id]['sapd'].append(sap_descriptor)
            self.data_project = current_data
            self.update()
            result = True
        except Exception as e:
            log.exception(e)
            result = False
        return result

    # NS operations: add/remove VNF
    def add_ns_vnf(self, ns_id, vnf_id):
        # Aggingi l'id a vnfProfile e aggiungi un entry in nsDf e creare il file descriptor del VNF
        try:
            current_data = json.loads(self.data_project)
            # utility = Util()
            current_data['nsd'][ns_id]['vnfdId'].append(vnf_id)
            vnf_profile = self.get_descriptor_template('nsd')['nsDf'][0]['vnfProfile'][0]
            vnf_profile['vnfdId'] = vnf_id
            current_data['nsd'][ns_id]['nsDf'][0]['vnfProfile'].append(vnf_profile)
            vnf_descriptor = self.get_descriptor_template('vnfd')
            vnf_descriptor['vnfdId'] = vnf_id
            vnf_descriptor['vdu'] = []
            vnf_descriptor['intVirtualLinkDesc'] = []
            vnf_descriptor['vnfExtCpd'] = []
            if 'vnfd' not in current_data:
                current_data['vnfd'] = {}
            current_data['vnfd'][vnf_id] = vnf_descriptor
            self.data_project = current_data
            self.update()
            result = True
        except Exception as e:
            log.exception(e)
            result = False
        return result

    def add_ns_existing_vnf(self, ns_id, vnf_id):
        try:
            current_data = json.loads(self.data_project)
            current_data['nsd'][ns_id]['vnfdId'].append(vnf_id)
            # utility = Util()
            vnf_profile = self.get_descriptor_template('nsd')['nsDf'][0]['vnfProfile'][0]
            vnf_profile['vnfdId'] = vnf_id
            current_data['nsd'][ns_id]['nsDf'][0]['vnfProfile'].append(vnf_profile)
            self.data_project = current_data
            self.update()
            result = True
        except Exception as e:
            log.exception(e)
            result = False
        return result

    def remove_ns_vnf(self, ns_id, vnf_id):
        try:
            current_data = json.loads(self.data_project)
            current_data['nsd'][ns_id]['vnfdId'].remove(vnf_id)
            vnf_profile = next(
                (x for x in current_data['nsd'][ns_id]['nsDf'][0]['vnfProfile'] if x['vnfdId'] == vnf_id), None)
            if vnf_profile is not None:
                current_data['nsd'][ns_id]['nsDf'][0]['vnfProfile'].remove(vnf_profile)
            self.data_project = current_data
            self.update()
            result = True
        except Exception as e:
            log.exception(e)
            result = False
        return result

    def edit_ns_vnf(self, vnf_id, vnf_descriptor):
        try:
            current_data = json.loads(self.data_project)
            if 'vnfd' not in current_data:
                current_data['vnfd'] = {}
            current_data['vnfd'][vnf_id] = vnf_descriptor
            self.data_project = current_data
            self.update()
            result = True
        except Exception as e:
            log.exception(e)
            result = False
        return result

    # NS operations: add/remove Nested NS
    def add_ns_nsNested(self, ns_id, nested_ns_id):
        try:
            current_data = json.loads(self.data_project)
            current_data['nsd'][ns_id]['nestedNsdId'].append(nested_ns_id)
            self.data_project = current_data
            self.update()
            result = True
        except Exception as e:
            log.exception(e)
            result = False
        return result

    # NS operations: link/Unlink Sap with VL
    def link_vl_sap(self, ns_id, vl_id, sap_id):
        try:
            current_data = json.loads(self.data_project)
            sap_descriptor = next((x for x in current_data['nsd'][ns_id]['sapd'] if x['cpdId'] == sap_id), None)
            if 'associatedCpdId' in sap_descriptor:
                del sap_descriptor['associatedCpdId']
            sap_descriptor['nsVirtualLinkDescId'] = vl_id
            self.data_project = current_data
            self.update()
            result = True
        except Exception as e:
            log.exception(e)
            result = False
        return result

    def unlink_vl_sap(self, ns_id, vl_id, sap_id):
        try:
            current_data = json.loads(self.data_project)
            sap_descriptor = next((x for x in current_data['nsd'][ns_id]['sapd'] if x['cpdId'] == sap_id), None)
            sap_descriptor['nsVirtualLinkDescId'] = None
            self.data_project = current_data
            self.update()
            result = True
        except Exception as e:
            log.exception(e)
            result = False
        return result

    # NS operations: link/Unlink vnf with VL
    def link_vnf_sap(self, ns_id, vnf_id, sap_id, ext_cp_id):
        try:
            current_data = json.loads(self.data_project)
            sap_descriptor = next((x for x in current_data['nsd'][ns_id]['sapd'] if x['cpdId'] == sap_id), None)
            if 'nsVirtualLinkDescId' in sap_descriptor:
                del sap_descriptor['nsVirtualLinkDescId']
            sap_descriptor['associatedCpdId'] = ext_cp_id
            self.data_project = current_data
            self.update()
            result = True
        except Exception as e:
            log.exception(e)
            result = False
        return result

    # NS operations: link/Unlink VNF with VL
    def link_vl_vnf(self, ns_id, vl_id, vnf_id, ext_cp_id):
        try:
            current_data = json.loads(self.data_project)
            # utility = Util()
            vnf_profile = next(
                (x for x in current_data['nsd'][ns_id]['nsDf'][0]['vnfProfile'] if x['vnfdId'] == vnf_id), None)
            virtual_link_profile = next((x for x in current_data['nsd'][ns_id]['nsDf'][0]['virtualLinkProfile'] if
                                         x['virtualLinkDescId'] == vl_id), None)
            if virtual_link_profile is None:
                virtual_link_profile = self.get_descriptor_template('nsd')['nsDf'][0]['virtualLinkProfile'][0]
                virtual_link_profile['virtualLinkDescId'] = vl_id
                current_data['nsd'][ns_id]['nsDf'][0]['virtualLinkProfile'].append(virtual_link_profile)
            virtual_link_profile_id = virtual_link_profile['virtualLinkProfileId']
            virtual_link_connectivity = next((x for x in vnf_profile['nsVirtualLinkConnectivity'] if
                                              x['virtualLinkProfileId'] == virtual_link_profile_id), None)
            if virtual_link_connectivity is not None:
                virtual_link_connectivity['cpdId'].append(ext_cp_id)
            else:
                virtual_link_connectivity = \
                    self.get_descriptor_template('nsd')['nsDf'][0]['vnfProfile'][0]['nsVirtualLinkConnectivity'][0]
                virtual_link_connectivity['virtualLinkProfileId'] = virtual_link_profile_id
                virtual_link_connectivity['cpdId'].append(ext_cp_id)
                vnf_profile['nsVirtualLinkConnectivity'].append(virtual_link_connectivity)
            self.data_project = current_data
            self.update()
            result = True
        except Exception as e:
            log.exception(e)
            result = False
        return result

    def unlink_vl_vnf(self, ns_id, vl_id, vnf_id):
        try:
            current_data = json.loads(self.data_project)
            # utility = Util()
            vnf_profile = next(
                (x for x in current_data['nsd'][ns_id]['nsDf'][0]['vnfProfile'] if x['vnfdId'] == vnf_id), None)
            virtual_link_profile = next((x for x in current_data['nsd'][ns_id]['nsDf'][0]['virtualLinkProfile'] if
                                         x['virtualLinkDescId'] == vl_id), None)
            virtual_link_profile_id = virtual_link_profile['virtualLinkProfileId']

            virtual_link_connectivity = next((x for x in vnf_profile['nsVirtualLinkConnectivity'] if
                                              x['virtualLinkProfileId'] == virtual_link_profile_id), None)
            if virtual_link_connectivity is not None:
                for vnfExtCpd in current_data['vnfd'][vnf_id]['vnfExtCpd']:

                    if vnfExtCpd['cpdId'] in virtual_link_connectivity['cpdId']:
                        log.debug("removing: %s", str(vnfExtCpd['cpdId']))
                        virtual_link_connectivity['cpdId'].remove(vnfExtCpd['cpdId'])
                if not virtual_link_connectivity['cpdId']:
                    vnf_profile['nsVirtualLinkConnectivity'].remove(virtual_link_connectivity)
            self.data_project = current_data
            self.update()
            result = True
        except Exception as e:
            log.exception(e)
            result = False
        return result

    # VNF operationd: add/remove VDU
    def add_vnf_vdu(self, vnf_id, vdu_id):
        try:
            current_data = json.loads(self.data_project)
            # utility = Util()
            vdu_descriptor = self.get_descriptor_template('vnfd')['vdu'][0]
            vdu_descriptor['vduId'] = vdu_id
            vdu_descriptor['intCpd'] = []
            current_data['vnfd'][vnf_id]['vdu'].append(vdu_descriptor)
            self.data_project = current_data
            self.update()
            result = True
        except Exception as e:
            log.exception(e)
            result = False
        return result

    def remove_vnf_vdu(self, vnf_id, vdu_id):
        try:
            current_data = json.loads(self.data_project)
            vdu_descriptor = next((x for x in current_data['vnfd'][vnf_id]['vdu'] if x['vduId'] == vdu_id), None)
            if vdu_descriptor is not None:
                current_data['vnfd'][vnf_id]['vdu'].remove(vdu_descriptor)
            self.data_project = current_data
            self.update()
            result = True
        except Exception as e:
            log.exception(e)
            result = False
        return result

    def edit_vnf_vdu(self, vnf_id, vdu_id, vdu_descriptor):
        try:
            current_data = json.loads(self.data_project)
            self.remove_vnf_vdu(vnf_id, vdu_id)
            current_data['vnfd'][vnf_id]['vdu'].append(vdu_descriptor)
            self.data_project = current_data
            self.update()
            result = True
        except Exception as e:
            log.exception(e)
            result = False
        return result

    # VNF operationd: add/remove CP VDU
    def add_vnf_vducp(self, vnf_id, vdu_id, vducp_id):
        try:
            current_data = json.loads(self.data_project)
            # utility = Util()
            vdu_descriptor = next((x for x in current_data['vnfd'][vnf_id]['vdu'] if x['vduId'] == vdu_id), None)
            intcp_descriptor = self.get_descriptor_template('vnfd')['vdu'][0]['intCpd'][0]
            intcp_descriptor['cpdId'] = vducp_id
            vdu_descriptor['intCpd'].append(intcp_descriptor)
            self.data_project = current_data
            self.update()
            result = True
        except Exception as e:
            log.exception(e)
            result = False
        return result

    def remove_vnf_vducp(self, vnf_id, vdu_id, vducp_id):
        try:
            current_data = json.loads(self.data_project)
            vdu_descriptor = next((x for x in current_data['vnfd'][vnf_id]['vdu'] if x['vduId'] == vdu_id), None)
            intcp_descriptor = next((x for x in vdu_descriptor['intCpd'] if x['cpdId'] == vducp_id), None)
            vdu_descriptor['intCpd'].remove(intcp_descriptor)
            self.data_project = current_data
            self.update()
            result = True
        except Exception as e:
            log.exception(e)
            result = False
        return result

    # VNF operationd: link/unlink VduCP and IntVL
    def link_vducp_intvl(self, vnf_id, vdu_id, vducp_id, intvl_id):
        try:
            current_data = json.loads(self.data_project)
            vdu_descriptor = next((x for x in current_data['vnfd'][vnf_id]['vdu'] if x['vduId'] == vdu_id), None)
            # TODO non capisco queste due righe qui sotto
            intcp_descriptor = next((x for x in vdu_descriptor['intCpd'] if x['cpdId'] == vducp_id), None)
            intcp_descriptor['intVirtualLinkDesc'] = intvl_id
            self.data_project = current_data
            self.update()
            result = True
        except Exception as e:
            log.exception(e)
            result = False
        return result

    def unlink_vducp_intvl(self, vnf_id, vducp_id, intvl_id):
        try:
            current_data = json.loads(self.data_project)
            for vdu in current_data['vnfd'][vnf_id]['vdu']:
                intCpd = next(
                    (x for x in vdu['intCpd'] if x['cpdId'] == vducp_id and x['intVirtualLinkDesc'] == intvl_id), None)
                if intCpd is not None:
                    intCpd['intVirtualLinkDesc'] = None
            self.data_project = current_data
            self.update()
            result = True
        except Exception as e:
            log.exception(e)
            result = False
        return result

    # VNF operationd: add/remove IntVL
    def add_vnf_intvl(self, vnf_id, intvl_id):
        try:
            current_data = json.loads(self.data_project)
            # utility = Util()
            intVirtualLinkDesc = self.get_descriptor_template('vnfd')['intVirtualLinkDesc'][0]
            intVirtualLinkDesc['virtualLinkDescId'] = intvl_id
            current_data['vnfd'][vnf_id]['intVirtualLinkDesc'].append(intVirtualLinkDesc)
            self.data_project = current_data
            self.update()
            result = True
        except Exception as e:
            log.exception(e)
            result = False
        return result

    def remove_vnf_intvl(self, vnf_id, intvl_id):
        try:
            current_data = json.loads(self.data_project)
            # utility = Util()
            intVirtualLinkDesc = next(
                (x for x in current_data['vnfd'][vnf_id]['intVirtualLinkDesc'] if x['virtualLinkDescId'] == intvl_id),
                None)
            current_data['vnfd'][vnf_id]['intVirtualLinkDesc'].remove(intVirtualLinkDesc)
            for vdu in current_data['vnfd'][vnf_id]['vdu']:
                for intCpd in vdu['intCpd']:
                    if intCpd['intVirtualLinkDesc'] == intvl_id:
                        intCpd['intVirtualLinkDesc'] = None
            for vnfExtCpd in current_data['vnfd'][vnf_id]['vnfExtCpd']:
                if vnfExtCpd['intVirtualLinkDesc'] == intvl_id:
                    vnfExtCpd['intVirtualLinkDesc'] = None
            for deploymentFlavour in current_data['vnfd'][vnf_id]['deploymentFlavour']:
                for virtualLinkProfile in deploymentFlavour['virtualLinkProfile']:
                    if virtualLinkProfile['vnfVirtualLinkDescId'] == intvl_id:
                        deploymentFlavour['virtualLinkProfile'].remove(virtualLinkProfile)
            self.data_project = current_data
            self.update()
            result = True
        except Exception as e:
            log.exception(e)
            result = False
        return result

    # VNF operationd: add/remove vnfExtCpd
    def add_vnf_vnfextcpd(self, vnf_id, vnfExtCpd_id):
        try:
            current_data = json.loads(self.data_project)
            # utility = Util()
            vnfExtCpd = self.get_descriptor_template('vnfd')['vnfExtCpd'][0]
            vnfExtCpd['cpdId'] = vnfExtCpd_id
            current_data['vnfd'][vnf_id]['vnfExtCpd'].append(vnfExtCpd)
            self.data_project = current_data
            self.update()
            result = True
        except Exception as e:
            log.exception(e)
            result = False
        return result

    def remove_vnf_vnfextcpd(self, vnf_id, vnfExtCpd_id):
        try:
            current_data = json.loads(self.data_project)
            # utility = Util()
            vnfExtCpd = next((x for x in current_data['vnfd'][vnf_id]['vnfExtCpd'] if x['cpdId'] == vnfExtCpd_id), None)
            current_data['vnfd'][vnf_id]['vnfExtCpd'].remove(vnfExtCpd)
            self.data_project = current_data
            self.update()
            result = True
        except Exception as e:
            log.exception(e)
            result = False
        return result

    # VNF operationd: link/unlink vnfextcpd and IntVL
    def link_vnfextcpd_intvl(self, vnf_id, vnfExtCpd_id, intvl_id):
        try:
            current_data = json.loads(self.data_project)
            vnfExtCpd = next((x for x in current_data['vnfd'][vnf_id]['vnfExtCpd'] if x['cpdId'] == vnfExtCpd_id), None)
            vnfExtCpd['intVirtualLinkDesc'] = intvl_id
            self.data_project = current_data
            self.update()
            result = True
        except Exception as e:
            log.exception(e)
            result = False
        return result

    def unlink_vnfextcpd_intvl(self, vnf_id, vnfExtCpd_id, intvl_id):
        try:
            current_data = json.loads(self.data_project)
            vnfExtCpd = next((x for x in current_data['vnfd'][vnf_id]['vnfExtCpd'] if x['cpdId'] == vnfExtCpd_id), None)
            vnfExtCpd['intVirtualLinkDesc'] = None
            self.data_project = current_data
            self.update()
            result = True
        except Exception as e:
            log.exception(e)
            result = False
        return result

    def add_vnffg(self, ns_id, vnffg_id):
        try:
            current_data = json.loads(self.data_project)
            # utility = Util()
            vnffg = self.get_descriptor_template('nsd')['vnffgd'][0]
            vnffg['vnffgdId'] = vnffg_id
            current_data['nsd'][ns_id]['vnffgd'].append(vnffg)
            self.data_project = current_data
            self.update()
            result = True
        except Exception as e:
            log.exception(e)
            result = False
        return result

    # def add_node_to_vnffg(self, ns_id, vnffg_id, element_type, element_id):
    def add_node_to_vnffg(self, request):
        try:
            group_id = request.POST.get('group_id')
            element_id = request.POST.get('element_id')
            element_type = request.POST.get('element_type')
            vnffg_id = request.POST.get('vnffg_id')
            # print group_id, element_id, element_type, vnffg_id

            current_data = json.loads(self.data_project)
            vnffg = next((x for x in current_data['nsd'][group_id]['vnffgd'] if x['vnffgdId'] == vnffg_id), None)
            if element_type == 'ns_vl':
                vnffg['virtualLinkDescId'].append(element_id)
            elif element_type == 'vnf':
                vnffg['vnfdId'].append(element_id)
            elif element_type == 'ns_cp':
                vnffg['cpdPoolId'].append(element_id)
            self.data_project = current_data
            self.update()
            result = True
        except Exception as e:
            log.exception(e)
            result = False
        return result

# Project.add_project_type('etsi', EtsiProject)
