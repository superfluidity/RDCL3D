import json
import requests
import logging

from deploymenthandler.helpers.helper import Helper
from lib.oshi.oshi_parser import OshiParser

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('oshi.py')


class OshiHelper(Helper):

    def launch(self, deployment):
        log.debug("OSHI DeploymentHelper launching deployment %d ", deployment.id)
        url = self.agent['base_url'] + "/deployments"

        r = self._send_post(url, json.dumps({'topology': deployment.deployment_descriptor, 'deployment_id': deployment.id}),
                         headers={'Content-type': 'application/json'})
        return r

    def stop(self,deployment_id=None):
        print "OSHI DeploymentHelper stop deployment %d ", deployment_id
        url = self.agent['base_url'] + "/deployments/" + str(deployment_id) + "/stop"
        r = self._send_post(url, headers={'Content-type': 'application/json'})
        return r




