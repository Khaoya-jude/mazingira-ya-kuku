from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="base/landing.html"), name="landing"),
    path("dashboard/", include("apps.accounts.urls", namespace="dashboard_root")),
    path("accounts/", include("apps.accounts.auth_urls", namespace="accounts")),
    path("feed/", include("apps.feed_watch.urls", namespace="feed_watch")),
    path("market/", include("apps.egg_market.urls", namespace="egg_market")),
    path("health/", include("apps.farm_guard.urls", namespace="farm_guard")),
    path("shop/", include("apps.trust_shop.urls", namespace="trust_shop")),
    path("learn/", include("apps.agri_learn.urls", namespace="agri_learn")),
    path("i18n/", include("django.conf.urls.i18n")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
