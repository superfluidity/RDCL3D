from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^base', views.base, name='basedev'),
]