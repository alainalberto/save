from django.conf.urls import url, include, url
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy

from  apps.administration.views import home_view
from  apps.administration.views_user import UserCreate, UserView


urlpatterns = [
    url(r'^user/', UserView.as_view(), name='users'),
    url(r'^user/create', UserCreate.as_view(), name='users_create'),
    url(r'^$', home_view, name='home'),

]
