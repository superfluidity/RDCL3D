from django.conf.urls import url, include
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^(?P<modelname>[a-z]+)$', views.get_model_specification),
]