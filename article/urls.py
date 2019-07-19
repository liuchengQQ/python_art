from django.conf.urls import url
from . import views,list_views

urlpatterns=[
     url(r'^article_column/$',views.article_column,name="article_column"),
     url(r'^rename_column/$',views.rename_article_column,name="rename_column"),
     url(r'^del_column/$',views.del_article_column,name="del_column"),
     url(r'^article_post/$',views.article_post,name="article_post"),
     url(r'^article_titles/$',list_views.article_titles,name="article_titles"),
     url(r'^list_article_title/(?P<id>\d+)/(?P<slug>[-\w]+)/$',list_views.article_detail,name="list_article_title"),
     url(r'^list_article_detail/(?P<username>[-\w]+)/$',list_views.article_detail,name="author_ticles"),
     url(r'^like_article/(?P<username>[-\w]+)/$',list_views.like_article,name="like_article"),
]

