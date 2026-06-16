from django.urls import path
from . import views
app_name = "trust_shop"
urlpatterns = [
    path("", views.supplier_directory, name="directory"),
    path("verify/<str:qr_token>/", views.verify_supplier, name="verify"),
    path("<int:pk>/", views.supplier_detail, name="detail"),
    path("<int:pk>/review/", views.add_review, name="add_review"),
]
