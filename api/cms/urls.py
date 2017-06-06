# coding:utf8

from django.conf.urls import url

import views

urlpatterns = [
    url(r'^$', views.article_manage, name='cms_index'),
    url(r'^article_manage/(?P<page>\d+)/(?P<category_id>\d+)/$',views.article_manage,name='cms_article_manage'),
    url(r'^login/$', views.cms_login, name='cms_login'),
    url(r'^logout/$', views.cms_logout, name='cms_logout'),
    url(r'^setting/$', views.cms_setting, name='cms_setting'),
    url(r'^update_profile/$', views.update_profile, name='cms_update_profile'),
    url(r'^update_email/$', views.update_email, name='cms_update_email'),
    url(r'^add_article/$', views.add_article, name='cms_add_article'),
    url(r'^update_article/(?P<pk>[\w\-]+)/$', views.update_article, name='cms_update_article'),
    url(r'^delete_article/$', views.delete_article, name='cms_delete_article'),
    url(r'^top_article/$', views.top_article, name='cms_top_article'),
    url(r'^untop_article/$', views.untop_article, name='cms_untop_article'),
    url(r'^add_category/$', views.add_category, name='cms_add_category'),
    url(r'^category_delete/$', views.category_delete, name='cms_category_delete'),
    url(r'^category_editer/$', views.category_editer, name='cms_category_editer'),
    url(r'^category_manage/$', views.category_manage, name='cms_category_manage'),
    url(r'^add_tag/$', views.add_tag, name='cms_add_tag'),
    url(r'^check_email/(?P<code>\w+)/$', views.check_email, name='cms_check_email'),
    url(r'^send_email_ok/$', views.send_email_ok, name='cms_send_email_ok'),
    url(r'^send_email_fail/$', views.send_email_fail, name='cms_send_email_fail'),
    url(r'^qiniu_token/$', views.qiniu_token, name='cms_qiniu_token'),
]