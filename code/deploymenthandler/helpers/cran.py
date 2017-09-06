import json
import logging

from deploymenthandler.helpers.helper import Helper
from projecthandler.models import Project

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('cran.py')


class DeploymentHelper(Helper):
    def launch(self, deployment):
        log.debug("CRAN DeploymentHelper launching deployment %d %s", deployment.id, deployment.descriptors_id)
        url = self.agent['base_url'] + "/deployments"
        projects = Project.objects.filter(id=deployment.project_id).select_subclasses()
        descriptor = projects[0].get_deployment_descriptor(descId=deployment.descriptors_id[0])
        deployment.deployment_descriptor = descriptor
        deployment.save()
        r = self._send_post(url, json.dumps(
            {'deployment_descriptor': descriptor, 'project_type': 'cran', 'deployment_type': deployment.type,
             'deployment_id': deployment.id}),
                            headers={'Content-type': 'application/json'})
        return r

    def stop(self, deployment_id=None):
        print "CRAN DeploymentHelper stop deployment %d ", deployment_id
        url = self.agent['base_url'] + "/deployments/" + str(deployment_id) + "/stop"
        r = self._send_post(url, headers={'Content-type': 'application/json'})
        return r
