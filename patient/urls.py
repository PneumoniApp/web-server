from django.urls import path
from . import views

urlpatterns= [
path("createPatient/",views.createPatient,name="createPatient"),
path("indexPatient/",views.indexPatient,name="indexPatient"),
path("viewPatient/<int:id>",views.viewPatient,name="viewPatient"),
path("editPatient/<int:id>",views.editPatient,name="editPatient"),
path("deletePatient/<int:id>",views.deletePatient,name="deletePatient"),
]