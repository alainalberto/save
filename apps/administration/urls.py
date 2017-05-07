from django.conf.urls import url, include

from  apps.administration.views import signin, home_wiew


urlpatterns = [
    #url(r'^$', signin),
    url(r'^$', home_wiew, name='home'),

]
