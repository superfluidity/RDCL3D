from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^base', views.base, name='basedev'),
    url(r'^d3js', views.d3js, name='d3js'),
    url(r'^topology_test', views.topology_test, name='topology_test')
]