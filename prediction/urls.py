from django.urls import path
from . import views

urlpatterns= [
path("createPrediction/",views.createPrediction,name="createPrediction"),
path("indexPrediction/",views.indexPrediction,name="indexPrediction"),
path("viewPrediction/<int:id>",views.viewPrediction,name="viewPrediction"),
path("deleteXray/<int:id>",views.deleteXray,name="deleteXray"),
path("deleteComment/<int:id>/<int:xray_id>",views.deleteComment,name="deleteComment"),
path("process_data_xray/<int:id>",views.process_data_xray,name="process_data_xray"),

]