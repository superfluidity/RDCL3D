import requests
import logging


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('helper.py')


class Helper():

    def __init__(self, agent):
        self.agent = agent
        pass

    def get_agent_status(self, args):
        log.debug("get status")
        url = self.agent['base_url'] + "/status"
        r = requests.get(url)
        return r.json()

    def open_shell(self, deployment_id, node_id):
        log.debug("open shell")
        url = self.agent['base_url'] + "/deployments/" + str(deployment_id) + "/node/" + str(node_id)
        r = requests.get(url)
        return r.json()

    def _send_post(self, url, data=None, json=None, **kwargs):
            try:
                r = requests.post(url, data=data, json=json, **kwargs)
            except Exception as e:
                return {'error': 'error during connection to agent'}
            return r.json()
