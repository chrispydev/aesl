from django.urls import path
from media_handle.views import ImageUploadView


urlpatterns = [
    path(
        "upload/",
        ImageUploadView.as_view(),
        name="image-upload",
    ),
    path(
        "upload/<int:image_id>/",
        ImageUploadView.as_view(),
        name="image-delete",
    ),
]
