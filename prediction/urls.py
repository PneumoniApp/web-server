from django.urls import path
from . import views

urlpatterns= [
path("createPrediction/",views.createPrediction,name="createPrediction"),
path("viewPrediction/<int:id>",views.viewPrediction,name="viewPrediction"),
]