from django.conf.urls import url
from nugu import views

urlpatterns = [
    url(r'^location$', views.location),
    url(r'^location/$', views.location)
]