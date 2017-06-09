import json
import logging
import requests
import yaml
from lib.util import Util
from deploymenthandler.helpers.helper import Helper
from projecthandler.models import Project

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('superfluidity.py')


class SuperfluidityHelper(Helper):

    def launch(self, deployment):
        log.debug("Superfluidity DeploymentHelper launching deployment %d %s", deployment.id, deployment.descriptors_id)
        url = self.agent['base_url'] + "/deployments"
        projects = Project.objects.filter(id=deployment.project_id).select_subclasses()
        descriptor = projects[0].get_deployment_descriptor(nsdId=deployment.descriptors_id[0])
        deployment.deployment_descriptor = descriptor
        deployment.save()
        r = self._send_post(url, json.dumps({'deployment_descriptor': descriptor, 'deployment_id': deployment.id}),
                         headers={'Content-type': 'application/json'})
        return r

    def stop(self, deployment_id=None):
        log.debug("Superfluidity DeploymentHelper stop deployment %d ", deployment_id)
        url = self.agent['base_url'] + "/deployments/" + str(deployment_id) + "/stop"
        r = self._send_post(url, headers={'Content-type': 'application/json'})
        return r

    def node_info(self, deployment_id, node_id):
        log.debug("get node info cRAN")
        log.debug("get node info")
        url = self.agent['base_url'] + "/deployments/" + str(deployment_id) + "/node/" + str(node_id)
        r = requests.get(url).json()
        # WARNING: expect openvim data
        if 'node_info' in r:
            splitted = r['node_info'].splitlines(True)[1:]
            joined = "".join(splitted)
            r['node_info'] = Util.yaml2json(yaml.load(joined))
        return r

