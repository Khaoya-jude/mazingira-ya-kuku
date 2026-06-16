# apps/feed_watch/urls.py
from django.urls import path
from . import views

app_name = "feed_watch"
urlpatterns = [
    path("prices/", views.price_list, name="prices"),
    path("prices/submit/", views.submit_price, name="submit_price"),
    path("bulk/", views.bulk_buy_list, name="bulk_buy"),
    path("bulk/create/", views.create_bulk_group, name="create_bulk"),
    path("bulk/<int:group_id>/join/", views.join_bulk_group, name="join_bulk"),
]
