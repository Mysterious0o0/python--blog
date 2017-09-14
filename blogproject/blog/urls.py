from django.conf.urls import url
from . import views
app_name = 'blog'
urlpatterns = [
#regular expression 正则表达式
    url(r'^$',views.IndexView.as_view(),name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$',views.detail,name = 'detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$',views.archives,name='archives')
]