from django.urls import path
from . import views

urlpatterns= [
path("",views.initial,name="initial"),
path("home/",views.home,name="home"),
path("create/",views.create,name="create"),
path("information/",views.information,name="information"),
path("password_reset", views.password_reset_request, name="password_reset")
]
