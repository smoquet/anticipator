from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^result$', views.result, name='result'),
    url(r'^victory$', views.victory, name='victory'),
    # views.vpgtest verwijst naar de functienaam
    url(r'^vpgtest$', views.vpgtest, name='vpgtest'),
    url(r'^callspot/$', views.callspot, name='callspot'),
]
