# apps/accounts/urls.py  (dashboard namespace)
from django.urls import path
from . import views

app_name = "dashboard_root"
urlpatterns = [
    path("", views.dashboard, name="home"),
    path("log/", views.log_record, name="log_record"),
    path("profile/", views.profile, name="profile"),
]
