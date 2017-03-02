from django.conf.urls import url
from django.contrib import admin

from . import views

app_name = "trading"

urlpatterns = [
	url(r'^$', views.index, name="index"),
	url(r'^query/?', views.query, name="query"),
	url(r'^purchase/?', views.purchase, name="purchase"),
	url(r'^login/?', views.login, name="login"),
	url(r'^register/?', views.register, name="register"),
	url(r'^logout/?', views.logout, name="logout"),
]
