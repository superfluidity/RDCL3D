import json
import requests
import logging

from deploymenthandler.helpers.helper import Helper
from lib.oshi.oshi_parser import OshiParser

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('oshi.py')


class OshiHelper(Helper):

    def launch(self, topology=None, deployment_id=None):
        log.debug("OSHI DeploymentHelper launching deployment %d ", deployment_id)
        url = self.agent['base_url'] + "/deployments"
        ###### TODO remove it just test need facility to build topology for deployment #####
        topology_data = OshiParser.importprojectdir('usecases/OSHI/example1', 'json')
        topology = topology_data['oshi']['example1']
        #####

        r = self._send_post(url, json.dumps({'topology': topology, 'deployment_id': deployment_id}),
                         headers={'Content-type': 'application/json'})
        return r

    def stop(self,deployment_id=None):
        log.debug("OSHI DeploymentHelper stop deployment %d ", deployment_id)
        url = self.agent['base_url'] + "/deployments/" + str(deployment_id) + "/stop"
        r = self._send_post(url, headers={'Content-type': 'application/json'})
        return r

    def get_deployment_info(self, deployment_id=None):
        url = self.agent['base_url'] + "/deployments/"+str(deployment_id)
        r = requests.get(url)
        return r.json()


