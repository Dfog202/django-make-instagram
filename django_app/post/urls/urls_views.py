from django.conf.urls import url
from .. import views

app_name = 'post'
urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^(?P<post_pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^create/$', views.post_create, name='post_create'),
    url(r'^(?P<post_pk>\d+)/modify/$', views.post_modify, name='post_modify'),
    url(r'^(?P<post_pk>\d+)/delete/$', views.post_delete, name='post_delete'),

    url(r'^(?P<post_pk>\d+)/comment/create/$', views.comment_create, name='comment_create'),
    url(r'^comment/(?P<comment_pk>\d+)/modify/$', views.comment_modify, name='comment_modify'),
    url(r'^comment/(?P<comment_pk>\d+)/delete/$', views.comment_delete, name='comment_delete'),

    url(r'tags/(?P<tag_name>\w+)/$', views.hashtag_post_list, name='hashtag_post_list'),
    url(r'^(?P<post_pk>\d+)/like/$', views.post_like_toggle, name='post_like_toggle'),

    url(r'^youtube/search/$', views.youtube_search, name='youtube_search'),
    url(r'^youtube/post/create/$', views.post_create_with_video, name='youtube_post_create'),
    # 위쪽의 결과들과 매칭되지 않을 경우
    # url(r'^.*/$', views.post_anyway, name='post_anyway'),
]

