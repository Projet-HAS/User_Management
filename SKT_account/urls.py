from django.contrib import admin
from django.urls import path

# import des views par défaut du système d'authentification
# de django, qui sera renommé auth_views
from django.contrib.auth import views as auth_views
from SKT_account import views

urlpatterns = [
  path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
  path('connection/', views.connectionHandler),
  path("users/create/", views.create_user_view, name="accounts:user_create"),
]
