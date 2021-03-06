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

from django.conf.urls import url
from projecthandler import views

urlpatterns = [
    url(r'^list/', views.repos_list, name='repos_list'),
    url(r'^new/', views.create_new_repo, name='new_repo'),
    url(r'^(?P<repo_id>\d+)/delete/', views.delete_repo, name='delete_repo'),
]