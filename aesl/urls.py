from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from frontend.admin_site import admin_site

urlpatterns = [
    path("admin/", admin_site.urls),
    path("", include("frontend.urls")),
    path("api/images/", include("media_handle.urls")),
    path(
        "api/",
        include("frontend.api_urls")
    ),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    path("__reload__/", include("django_browser_reload.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
