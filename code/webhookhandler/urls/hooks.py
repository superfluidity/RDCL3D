from django.conf.urls import url
from webhookhandler import views

urlpatterns = [
    url(r'^$', views.webhook, name='webhook'),
]