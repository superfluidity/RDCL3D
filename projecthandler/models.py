from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
import jsonfield
import json
# Create your models here.


class Project(models.Model):

    owner = models.ForeignKey('sf_user.CustomUser', db_column='owner')
    name = models.CharField(max_length=20)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now, blank=True, null=True)
    info = models.TextField(default='No info')
    data_project = jsonfield.JSONField(default={'nsd':{}, 'vld':{}, 'vnfd':{}, 'vnffgd': {}})
    validated = models.BooleanField(default=False)

    def get_dataproject(self):
        return self.data_project

    def get_overview_data(self):
        print  len(self.data_project['vnffgd'].keys()) if 'vnffgd' in self.data_project else 0
        result = {
            'owner': self.owner,
            'name': self.name,
            'updated_date': self.updated_date,
            'info': self.info,
            'nsd': len(self.data_project['nsd'].keys()) if 'nsd' in self.data_project else 0,
            'vnffgd': len(self.data_project['vnffgd'].keys()) if 'vnffgd' in self.data_project else 0,
            'vld': len(self.data_project['vld'].keys()) if 'vld' in self.data_project else 0,
            'vnfd': len(self.data_project['vnfd'].keys()) if 'vnfd' in self.data_project else 0,
            'validated': self.validated
        }
        print result
        return result

    def get_descriptors(self, type_descriptor):
        try:
            ##FIXME nsd dovrebbe essere in forma dict come gli altri
            #if(type_descriptor == 'nsd'):
            #    result = {self.data_project['nsd']['name']: self.data_project['nsd']}
            #else:
            #    result = self.data_project[type_descriptor]
            result = self.data_project[type_descriptor]
        except Exception as e:
            result = {}
        return result

    def get_descriptor(self, descriptor_id, type_descriptor):
        result = {}

        try:
            result = self.data_project[type_descriptor][descriptor_id]
        except:
            result = {}

        return result

    def set_validated(self, value):
        self.validated = True if value is not None and value == True else False

    def set_data_project(self, new_data, validated):
        #self.data_project = new_data
        self.set_validated(validated)
        self.update()

    def update(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name