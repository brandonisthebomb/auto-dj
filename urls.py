from django.conf.urls import url, include
from django.contrib import admin

from . import views

urlpatterns = [
	url(r'^$', views.index, name="index"),
	url(r'^beats/$', views.beats, name="beats"),
	url(r'^beats/callback$', views.beats_callback, name="beats_callback"),
]