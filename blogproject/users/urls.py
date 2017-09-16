from django.conf.urls import url

from . import views
app_name = 'users'
urlpatterns = [
    #http://127.0.0.1:8000/accounts/register
    url(r'^register/',views.register,name='register')
]