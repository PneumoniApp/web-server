from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns= [
path("",views.initial,name="initial"),
path("home/",views.home,name="home"),
path("create/",views.create,name="create"),
path("information/",views.information,name="information"),
path("password_reset", views.password_reset_request, name="password_reset"),
path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='main/password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="main/password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='main/password/password_reset_complete.html'), name='password_reset_complete'),
]
