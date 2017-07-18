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
    url(r'^list/', views.user_projects, name='projects_list'),
    url(r'^new/', views.create_new_project, name='new_project'),
    url(r'^(?P<project_id>\d+)/$', views.open_project, name='open_project'),
    url(r'^(?P<project_id>\d+)/push_project$', views.push_project, name='push_project'),
    url(r'^(?P<project_id>\d+)/delete$', views.delete_project, name='delete_project'),
    url(r'^(?P<project_id>\d+)/graph(/$)', views.graph, name='graph_view'),
    url(r'^(?P<project_id>\d+)/graph/graph_data(/$)', views.graph_data, name='graph_data'),
    url(r'^(?P<project_id>\d+)/graph/graph_data/(?P<descriptor_id>[-\w]+)(/$)', views.graph_data, name='graph_data'),
    url(r'^(?P<project_id>\d+)/graph/positions$', views.graph_positions, name='graph_positions'),
    url(r'^(?P<project_id>\d+)/graph/unusedvnf/(?P<nsd_id>\w+)(/$)', views.unused_vnf, name='unused_vnf'),
    url(r'^(?P<project_id>\d+)/graph/addelement$', views.add_element, name='addelement'),
    url(r'^(?P<project_id>\d+)/graph/overviewelement$', views.overviewelement, name='overviewelement'),
    url(r'^(?P<project_id>\d+)/graph/addnodetovnffg', views.add_node_to_vnffg, name='addnodetovnffg'),
    url(r'^(?P<project_id>\d+)/graph/removeelement$', views.remove_element, name='removeelement'),
    url(r'^(?P<project_id>\d+)/graph/addlink$', views.add_link, name='addlink'),
    url(r'^(?P<project_id>\d+)/graph/removelink$', views.remove_link, name='removelink'),
    url(r'^(?P<project_id>\d+)/graph/availablenodes', views.get_available_nodes, name='get_available_nodes'),
    url(r'^(?P<project_id>\d+)/download(/$)', views.download, name='download_page'),
    url(r'^(?P<project_id>\d+)/descriptors/(?P<descriptor_type>\w+)(/$)', views.show_descriptors,
        name='show_descriptors'),
    url(r'^(?P<project_id>\d+)/descriptors/(?P<descriptor_type>\w+)/(?P<descriptor_id>[-\w]+)(/$)',
        views.edit_descriptor, name='edit_descriptor'),
    url(r'^(?P<project_id>\d+)/descriptors/(?P<descriptor_type>\w+)/(?P<descriptor_id>[-\w]+)/delete$',
        views.delete_descriptor,
        name='delete_descriptor'),
    url(r'^(?P<project_id>\d+)/descriptors/(?P<descriptor_type>\w+)/(?P<descriptor_id>[-\w]+)/clone$',
        views.clone_descriptor,
        name='clone_descriptor'),
    url(r'^(?P<project_id>\d+)/descriptors/(?P<descriptor_type>\w+)/(?P<descriptor_id>[-\w]+)/action/(?P<action_name>[-\w]+)',
        views.custom_action,
        name='custom_action'),
    url(r'^(?P<project_id>\d+)/descriptors/(?P<descriptor_type>\w+)/new$', views.new_descriptor,
        name='new_descriptor'),


]