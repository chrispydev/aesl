from django.urls import path
from frontend.views import HomeView, ProjectDetailView, ProjectView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("projects/", ProjectView.as_view(), name="projects"),
    path("project/<int:pk>/", ProjectDetailView.as_view(), name="project_detail"),
]
