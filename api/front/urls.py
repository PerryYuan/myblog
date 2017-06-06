# coding:utf8


from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.article_list,name='front_index'),
    url(r'^login/$', views.front_login,name='front_login'),
    url(r'^regist/$', views.regist,name='front_regist'),
    url(r'^search/$', views.search,name='front_search'),
    url(r'^forget_password/$', views.forget_password,name='front_forget_password'),
    url(r'^front_comment/$', views.front_comment,name='front_comment'),
    url(r'^reset_password/(?P<code>\w+)/$', views.reset_password,name='front_reset_password'),
    url(r'^check_email/(?P<code>\w+)/$', views.check_email,name='front_check_email'),
    url(r'^article_list/(?P<category_id>\d+)/(?P<page>\d+)/$', views.article_list,name='front_article_list'),
    url(r'^article_detail/(?P<article_id>[\w\-]+)/$', views.article_detail,name='front_article_detail'),
]