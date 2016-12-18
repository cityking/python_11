from django.conf.urls import url
from blog_app import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^archive/$', views.archive, name='archive'),
    url(r'^article/$', views.article, name='article'),
    url(r'^comment_post/$', views.comment_post, name='comment_post'),
]
