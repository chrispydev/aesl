from django.urls import path
from frontend.views import HomeView, ProjectView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("projects/", ProjectView.as_view(), name="projects"),
]
