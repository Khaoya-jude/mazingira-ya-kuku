# apps/accounts/auth_urls.py
from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path("login/", views.farmer_login, name="login"),
    path("logout/", views.farmer_logout, name="logout"),
    path("register/", views.register, name="register"),
]
