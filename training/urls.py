from django.conf.urls import url

from . import views

urlpatterns = [
    url('^$', views.index, name='index'),
    url('^train/(?P<training_session_id>[0-9]+)/$', views.train, name='train'),
]
