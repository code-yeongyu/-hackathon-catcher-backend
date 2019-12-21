from django.conf.urls import url
from family import views

urlpatterns = [
    url(r'^invite/$', views.invite),
    url(r'^join/$', views.join),
    url(r'^secede/$', views.secede),
    url(r'^members/$', views.members)
]