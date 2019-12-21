from django.conf.urls import url
from custom_account import views
from rest_framework.authtoken import views as drf_views

urlpatterns = [
    url(r'^signin/$', drf_views.obtain_auth_token, name='auth'),
    url(r'^signup/$', views.signup),
    url(r'^search/(?P<query>\w+)/$', views.search),
    url(r'^image/(?P<string>\w+)/$', views.image),
    url(r'^$', views.AccountAPIView.as_view()),
]