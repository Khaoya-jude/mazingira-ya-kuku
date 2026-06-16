from django.urls import path
from . import views

app_name = "farm_guard"
urlpatterns = [
    path("alerts/", views.alert_map, name="alerts"),
    path("alerts/report/", views.report_alert, name="report_alert"),
    path("symptom-checker/", views.symptom_checker, name="symptom_checker"),
    path("vaccinations/", views.vaccination_log, name="vaccination_log"),
]
