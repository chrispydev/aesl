from django.urls import path

from .views import NavbarSearchAPIView


urlpatterns = [

    path(
        "search/",
        NavbarSearchAPIView.as_view(),
        name="navbar_search"
    ),

]
