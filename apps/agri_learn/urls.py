from django.urls import path
from . import views
app_name = "agri_learn"
urlpatterns = [
    path("", views.article_list, name="articles"),
    path("article/<slug:slug>/", views.article_detail, name="article"),
    path("vets/", views.vet_directory, name="vets"),
    path("ask/", views.ask_expert, name="ask_expert"),
]
