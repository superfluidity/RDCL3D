import requests
import logging
import json
from lib.util import Util
import hashlib


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('helper.py')


class Client(object):
    def __init__(self, host=None, so_port=9999, so_project='admin', ro_host=None, ro_port=9090, **kwargs):

        self._user = 'admin'
        self._password = 'admin'
        # self._project = so_project
        self._project = so_project
        self._auth_endpoint = '/token/v1'
        self._headers = {}
        # if len(host.split(':')) > 1:
        #     # backwards compatible, port provided as part of host
        #     self._host = host.split(':')[0]
        #     self._so_port = host.split(':')[1]
        # else:
        #     self._host = host
        #     self._so_port = so_port

        if ro_host is None:
            ro_host = host

    def get_token(self):
        postfields_dict = {'username': self._user,
                           'password': self._password,
                           'project-id': self._project}
        token = self._send_post('https://40.86.191.138:9999/osm/token/v1', None, postfields_dict, headers={"Content-Type": "application/yaml", "accept": "application/json"})
        if token is not None:
            return token['id']
        return None

    def nsd_list(self):
        token = self.get_token()
        if token:
            self._headers['Authorization'] = 'Bearer {}'.format(token)
            self._headers['Content-Type'] = 'application/yaml'
            self._headers['accept'] = 'application/json'
            return self._send_get("https://40.86.191.138:9999/osm/nsd/v1/ns_descriptors", headers=self._headers)
        return None

    def nsd_get(self, id):
        token = self.get_token()
        if token:
            self._headers['Authorization'] = 'Bearer {}'.format(token)
            self._headers['Content-Type'] = 'application/yaml'
            self._headers['accept'] = 'application/json'
            return self._send_get("https://40.86.191.138:9999/osm/nsd/v1/ns_descriptors/{}".format(id), headers=self._headers)
        return None

    def nsd_delete(self, id):
        token = self.get_token()
        if token:
            self._headers['Authorization'] = 'Bearer {}'.format(token)
            self._headers['Content-Type'] = 'application/yaml'
            self._headers['accept'] = 'application/json'
            return self._send_delete("https://40.86.191.138:9999/osm/nsd/v1/ns_descriptors/{}".format(id), headers=self._headers)
        return None

    def nsd_onboard(self, package):
        token = self.get_token()
        headers = {}
        if token:

            headers['Authorization'] = 'Bearer {}'.format(token)
            headers['Content-Type'] = 'application/gzip'
            #headers['Content-File-MD5'] = self.md5file('cirros_2vnf_ns.tar.gz')
            #print self.md5(package.file)
            #print self.md5file('cirros_2vnf_ns.tar.gz')
            #files = {'file': ('cirros_2vnf_ns.tar.gz', open('cirros_2vnf_ns.tar.gz', 'rb'), 'application/gzip')}
            #print headers['Content-File-MD5']
            headers['accept'] = 'application/json'
            #print package.read()
            #print (package.name)
            with open('/tmp/'+package.name, 'wb+') as destination:
                for chunk in package.chunks():
                    destination.write(chunk)
            headers['Content-File-MD5'] = self.md5(open('/tmp/'+package.name, 'rb'))
            #print type(open('cirros_2vnf_ns.tar.gz', 'rb').read())
            #r = requests.post(url='http://upload.example.com', data={'title': 'test_file},  files =  {'file':package})
            return self._send_post("https://40.86.191.138:9999/osm/nsd/v1/ns_descriptors", headers=headers,
                                  data=open('/tmp/'+package.name, 'rb'))
        return None

    def vnfd_list(self):
        token = self.get_token()
        if token:
            self._headers['Authorization'] = 'Bearer {}'.format(token)
            self._headers['Content-Type'] = 'application/yaml'
            self._headers['accept'] = 'application/json'
            return self._send_get("https://40.86.191.138:9999/osm/vnfpkgm/v1/vnf_packages", headers=self._headers)
        return None

    def vnfd_get(self, id):
        token = self.get_token()
        if token:
            self._headers['Authorization'] = 'Bearer {}'.format(token)
            self._headers['Content-Type'] = 'application/yaml'
            self._headers['accept'] = 'application/json'
            return self._send_get("https://40.86.191.138:9999/osm/vnfpkgm/v1/vnf_packages/{}".format(id), headers=self._headers)
        return None

    def vnfd_delete(self, id):
        token = self.get_token()
        if token:
            self._headers['Authorization'] = 'Bearer {}'.format(token)
            self._headers['Content-Type'] = 'application/yaml'
            self._headers['accept'] = 'application/json'
            return self._send_delete("https://40.86.191.138:9999/osm/vnfpkgm/v1/vnf_packages/{}".format(id), headers=self._headers)
        return None

    def vnfd_onboard(self, package):
        token = self.get_token()
        headers = {}
        if token:
            headers['Authorization'] = 'Bearer {}'.format(token)
            headers['Content-Type'] = 'application/gzip'
            headers['accept'] = 'application/json'
            with open('/tmp/'+package.name, 'wb+') as destination:
                for chunk in package.chunks():
                    destination.write(chunk)
            headers['Content-File-MD5'] = self.md5(open('/tmp/'+package.name, 'rb'))
            return self._send_post("https://40.86.191.138:9999/osm/vnfpkgm/v1/vnf_packages", headers=headers,
                                   data=open('/tmp/' + package.name, 'rb'))
        return None

    def _upload_package(self, filename, package):
        token = self.get_token()
        headers = {}
        if token:
            headers['Authorization'] = 'Bearer {}'.format(token)
            headers['Content-Type'] = 'application/gzip'
            headers['Content-File-MD5'] = self.md5(package)
            headers['accept'] = 'application/json'
        return None

    def _send_post(self, url, data=None, json=None, **kwargs):
        try:
            r = requests.post(url, data=data, json=json, verify=False, **kwargs)
            print r.text
        except Exception as e:
            log.exception(e)
            print "Exception during send POST"
            return {'error': 'error during connection to agent'}
        return Util.json_loads_byteified(r.text)

    def _send_get(self, url, params=None, **kwargs):
        try:
            r = requests.get(url, params=None, verify=False, **kwargs)
        except Exception as e:
            log.exception(e)
            print "Exception during send GET"
            return {'error': 'error during connection to agent'}
        return Util.json_loads_byteified(r.text)

    def _send_delete(self, url, params=None, **kwargs):
        try:
            r = requests.delete(url, params=None, verify=False, **kwargs)
        except Exception as e:
            log.exception(e)
            print "Exception during send DELETE"
            return {'error': 'error during connection to agent'}
        return Util.json_loads_byteified(r.text)

    def md5(self, f):
        #hash_md5 = hashlib.md5()
        #with open(fname, "rb") as f:
        #    for chunk in iter(lambda: f.read(4096), b""):
        #        hash_md5.update(chunk)
        #return hash_md5.hexdigest()
        hash_md5 = hashlib.md5()
        for chunk in iter(lambda: f.read(1024), b""):
            hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def md5file(self, fname):
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
           for chunk in iter(lambda: f.read(1024), b""):
               hash_md5.update(chunk)
        return hash_md5.hexdigest()
