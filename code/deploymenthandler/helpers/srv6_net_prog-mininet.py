import json
import logging

from deploymenthandler.helpers.helper import Helper
from projecthandler.models import Project

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('srv6_net_prog.py')

class DeploymentHelper(Helper):
    def launch(self, deployment):
        log.debug("SRV6 DeploymentHelper launching deployment %d %s", deployment.id, deployment.descriptors_id)
        url = self.agent['base_url'] + "/deployments"
        projects = Project.objects.filter(id=deployment.project_id).select_subclasses()
        descriptor = projects[0].get_descriptor(deployment.descriptors_id[0], 'srv6_net_prog')
        deployment.deployment_descriptor = descriptor;
        deployment.save()

       # with open('data.txt', 'w') as outfile:
       #     json.dump(descriptor, outfile)

        r = self._send_post(url, json.dumps({'deployment_descriptor': descriptor,
                                             'project_type': 'srv6_net_prog', 'deployment_type': deployment.type,
                                             'deployment_id': deployment.id}),
                            headers={'Content-type': 'application/json'})
        return r

    def stop(self, deployment_id=None):
        print "SRV6_NET_PROG DeploymentHelper stop deployment %d ", deployment_id
        url = self.agent['base_url'] + "/deployments/" + str(deployment_id) + "/stop"
        r = self._send_post(url, headers={'Content-type': 'application/json'})
        return r
