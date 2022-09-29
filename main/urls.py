from django.urls import path
from . import views

urlpatterns= [
path("<int:id>",views.index, name="index"),
path("",views.initial,name="initial"),
path("home/",views.home,name="home"),
path("create/",views.create,name="create"),
path("information/",views.information,name="information"),

]
