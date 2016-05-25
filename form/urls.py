from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # views.vpgtest verwijst naar de functienaam
    url(r'^vpgtest$', views.vpgtest, name='vpgtest'),
    url(r'^callspot/$', views.callspot, name='callspot'),
]
