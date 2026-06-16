# apps/egg_market/urls.py
from django.urls import path
from . import views as em_views
app_name = "egg_market"
urlpatterns = [
    path("listings/", em_views.listing_list, name="listings"),
    path("listings/new/", em_views.create_listing, name="create_listing"),
    path("listings/<int:pk>/", em_views.listing_detail, name="listing_detail"),
    path("prices/", em_views.market_prices, name="market_prices"),
]
