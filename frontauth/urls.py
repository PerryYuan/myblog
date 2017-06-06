# coding:utf8

from django.conf.urls import url,include
import views
urlpatterns = [
    url(r'^add_front_user/$', views.add_front_user),
    url(r'^login/$', views.test),
    url(r'^logout/$', views.test1),
    url(r'^test2/$', views.test2),

]