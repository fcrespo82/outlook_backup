from django.conf.urls import patterns, url 
from outlook_backup_app import views 

urlpatterns = patterns('', 
  url(r'^$', views.home, name='home'), 
  url(r'^home/$', views.home, name='home'),
  url(r'^gettoken/$', views.gettoken, name='gettoken'),
  # Mail view ('/tutorial/mail/')>
  url(r'^mail/$', views.mail, name='mail'),
  url(r'^mail/preview/$', views.preview, name='preview'),
) 
