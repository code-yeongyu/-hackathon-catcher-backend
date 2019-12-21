from django.conf.urls import url
from nugu import views

urlpatterns = [
    url(r'^Location_action$', views.location),
    url(r'^connection$', views.HeasunFa)
]
