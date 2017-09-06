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

import jsonfield
from django.db import models
from django.utils import timezone
import logging
import importlib
import json

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('models.py')


class DeployAgent(models.Model):
    """ DeployAgent
    """
    name = models.CharField(max_length=20, default='')
    base_url = models.TextField(default='')
    #type = models.CharField(max_length=20, default='')
    last_update = models.DateTimeField(default=timezone.now)

    def to_json(self):
        return {
            'name': self.name,
            'base_url': self.base_url.rstrip('\/'),
            #'type': self.type,
            'last_update': self.last_update
        }


class Deployment(models.Model):
    """ Base class for Deployment types

    """
    name = models.CharField(max_length=20, default='')
    profile = jsonfield.JSONField(default={})
    #project = models.ForeignKey('projecthandler.Project', db_column='project_id')
    project_type = models.CharField(max_length=20, default='')
    project_name = models.CharField(max_length=20, default='')
    project_id = models.CharField(max_length=20, default='')
    creator = models.ForeignKey('sf_user.CustomUser', db_column='creator_id')
    created_date = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=20, default='')
    status = models.CharField(max_length=20, default='')
    descriptors_id = jsonfield.JSONField(default=[])
    deployment_agent = jsonfield.JSONField(default={})
    """Stores a JSON representation of the deployment agent info"""
    deployment_descriptor = jsonfield.JSONField(default={})
    """Stores a validated JSON representation of the deployment descriptor"""

    def create(self, *args, **kwargs):
        if 'type' in kwargs and isinstance(kwargs['type'], basestring):
            kwargs['type'] = Deployment.objects.get(name=kwargs['type'])
        return super(Deployment, self).create(*args, **kwargs)

    def launch(self):
        log.debug("launch Deployment")
        HelperClass = self._getHelperClass()
        deploy = HelperClass(self.deployment_agent)

        result = deploy.launch(self)
        if 'error' not in result:
            self.status = "running"
        else:
            self.status = "not started"
        self.save()
        return result

    def stop(self):
        log.debug("stop Deployment")
        HelperClass = self._getHelperClass()
        deploy = HelperClass(self.deployment_agent)
        return deploy.stop(deployment_id=self.id)

    def delete(self, *args, **kwargs):
        print "delete Deployment"
        self.stop()
        super(Deployment, self).delete(*args, **kwargs)

    def get_status(self):
        log.debug("Deployment get status")
        HelperClass = self._getHelperClass()
        deploy = HelperClass(self.deployment_agent)
        return deploy.get_deployment_status(deployment_id=self.id)

    def get_info(self):
        log.debug("Deployment get info")
        HelperClass = self._getHelperClass()
        deploy = HelperClass(self.deployment_agent)
        result = deploy.get_deployment_info(deployment_id=self.id)
        if 'error' not in result:
            self.deployment_descriptor = json.dumps(result['deployment_descriptor'])
            self.save()
        return result


    def open_shell(self, node_id=None):
        log.debug("Deployment open shell - get info about shell")
        HelperClass = self._getHelperClass()
        deploy = HelperClass(self.deployment_agent)
        return deploy.open_shell(self.id, node_id)

    def node_info(self, node_id=None):
        log.debug("Deployment node info - get info about node")
        HelperClass = self._getHelperClass()
        deploy = HelperClass(self.deployment_agent)
        return deploy.node_info(self.id, node_id)

    def _getHelperClass(self):
        my_module = importlib.import_module("deploymenthandler.helpers."+self.type)
        HelperClass = getattr(my_module,  "DeploymentHelper")

        return HelperClass

    def to_json(self):
        return {
            'name': self.name,
            'profile': self.profile,
            'type': self.type,
            'project_id': self.project_id,
            'project_name': self.project_name,
            'project_type': self.project_name,
            'creator_id': self.creator.id,
            'creator_name': str(self.creator.get_full_name()),
            'created_date': str(self.created_date),
            'last_update': str(self.last_update),
            'status': self.status,
            'deployment_agent': self.deployment_agent,
            'deployment_descriptor':  self.deployment_descriptor
        }
