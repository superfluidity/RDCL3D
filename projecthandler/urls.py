
from django.conf.urls import url, include
from django.contrib import admin
from projecthandler import views

urlpatterns = [
    url(r'^table/', views.user_projects, name='projects_list'),
    url(r'^new/', views.create_new_project, name='new_project'),
    url(r'^(?P<project_id>\d+)/$', views.open_project, name='open_project'),
    url(r'^(?P<project_id>\d+)/delete$', views.delete_project, name='delete_project'),
    url(r'^(?P<project_id>\d+)/graph(/$)', views.graph, name='graph_view'),
    url(r'^(?P<project_id>\d+)/graph/graph_data(/$)', views.graph_data, name='graph_data'),
    url(r'^(?P<project_id>\d+)/graph/positions$', views.graph_positions, name='graph_positions'),
    url(r'^(?P<project_id>\d+)/graph/sap$', views.sap, name='sap'),
    url(r'^(?P<project_id>\d+)/download(/$)', views.downlaod, name='download_page'),
    url(r'^(?P<project_id>\d+)/descriptors/(?P<descriptor_type>\w+)(/$)', views.show_descriptors, name='show_descriptors'),
    url(r'^(?P<project_id>\d+)/descriptors/(?P<descriptor_type>\w+)/(?P<descriptor_id>[-\w]+)(/$)', views.edit_descriptor, name='edit_descriptor'),
    url(r'^(?P<project_id>\d+)/descriptors/(?P<descriptor_type>\w+)/(?P<descriptor_id>[-\w]+)/delete$', views.delete_descriptor,
        name='delete_descriptor'),
    url(r'^(?P<project_id>\d+)/descriptors/(?P<descriptor_type>\w+)/new$', views.new_descriptor,
             name='new_descriptor'),

]
