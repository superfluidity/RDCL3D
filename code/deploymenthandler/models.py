#
#   Copyright 2017 CNIT - Consorzio Nazionale Interuniversitario per le Telecomunicazioni
#
#   Licensed under the Apache License, Version 2.0 (the );
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


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('models.py')

project_types = {}


class DeployAgent(models.Model):
    """ DeployAgent
    """
    name = models.CharField(max_length=20, default='')
    base_url = models.TextField(default='')
    type = models.CharField(max_length=20, default='')
    last_update = models.DateTimeField(default=timezone.now)


class Deployment(models.Model):
    """ Base class for Deployment types

    """
    name = models.CharField(max_length=20, default='')
    profile = jsonfield.JSONField(default={})
    project_name = models.CharField(max_length=20, default='')
    project_id = models.CharField(max_length=20, default='')
    creator_name = models.CharField(max_length=20, default='')
    creator_id = models.CharField(max_length=20, default='')
    created_date = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, default='')
    agent = DeployAgent



