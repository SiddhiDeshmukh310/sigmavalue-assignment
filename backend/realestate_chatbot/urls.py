from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
]

# Serve STATIC FILES from React build
urlpatterns += [
    re_path(
        r"^static/(?P<path>.*)$",
        serve,
        {"document_root": settings.BASE_DIR / "frontend_build" / "static"},
    ),
]

# Serve favicon
urlpatterns += [
    re_path(
        r"^favicon\.svg$",
        serve,
        {"document_root": settings.BASE_DIR / "frontend_build", "path": "favicon.svg"},
    )
]

# Serve manifest.json
urlpatterns += [
    re_path(
        r"^manifest\.json$",
        serve,
        {"document_root": settings.BASE_DIR / "frontend_build", "path": "manifest.json"},
    )
]

# React SPA handler (catch-all)
urlpatterns += [
    re_path(r"^.*$", TemplateView.as_view(template_name="index.html")),
]
