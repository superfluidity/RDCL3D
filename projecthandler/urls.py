
from django.conf.urls import url, include
from django.contrib import admin
from projecthandler import views

urlpatterns = [
    url(r'^table/', views.user_projects, name='projects_list'),
    url(r'^create_test/', views.create_project),
    url(r'^new/', views.create_new_project, name='new_project'),
    url(r'^(?P<project_id>\d+)/$', views.open_project, name='open_project'),
    url(r'^(?P<project_id>\d+)/graph(/$)', views.graph, name='graph_view'),
    url(r'^(?P<project_id>\d+)/graph/graph_data(/$)', views.graph_data, name='graph_data'),
    url(r'^(?P<project_id>\d+)/download(/$)', views.downlaod, name='download'),
    url(r'^(?P<project_id>\d+)/descriptors/(?P<descriptor_type>\w+)(/$)', views.show_descriptors, name='show_descriptors'),
    url(r'^(?P<project_id>\d+)/descriptors/(?P<descriptor_type>\w+)/(?P<descriptor_id>\w+)(/$)', views.edit_descriptor, name='edit_descriptor'),

]
