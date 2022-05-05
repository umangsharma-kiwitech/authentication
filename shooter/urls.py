from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home.as_view(), name="home"),
    path('signup', views.signup.as_view(), name="signup"),
    path('signin', views.signin.as_view(), name="signin"),
    path('signout', views.signout, name="signout"),
    path('activate/<uid>/<token>', views.activate.as_view(), name='activate')

]
