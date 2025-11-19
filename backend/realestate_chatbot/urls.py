# backend/realestate_chatbot/urls.py
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]

# Serve static files first (CSS/JS from React build)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Catch-all for React app (must be LAST)
urlpatterns += [
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
]
