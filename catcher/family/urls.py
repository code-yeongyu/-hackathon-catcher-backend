from django.conf.urls import url
from family import views

urlpatterns = [
    url(r'^new_member/$', views.new_member),
    url(r'^$', views.FamilyCreation.as_view()),
]