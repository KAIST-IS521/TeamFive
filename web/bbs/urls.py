from django.conf.urls import url
from . import views

urlpatterns = (
    url(r'^$', views.index, name='index'),
    url(r'^list/', views.list, name='list'),
    url(r'^home/', views.home, name='home'),
    url(r'^write/', views.write, name='write'),
    url(r'^auth/$', views.auth_index, name='auth_index'),
    url(r'^auth/chal/$', views.auth_chal, name='auth_chal'),
    url(r'^auth/resp/$', views.auth_resp, name='auth_resp'),
)
