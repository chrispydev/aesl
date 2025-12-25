from django.urls import path
from frontend.views import (
    CorporateGovernaceView,
    HomeView,
    ManagementView,
    PracticeView,
    ProjectDetailView,
    ProjectView,
    SectorMinistryView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("projects/", ProjectView.as_view(), name="projects"),
    path("project/<int:pk>/", ProjectDetailView.as_view(), name="project_detail"),
    path("practice/", PracticeView.as_view(), name="practice"),
    path(
        "practice/sector-ministry/",
        SectorMinistryView.as_view(),
        name="sector_ministry",
    ),
    path(
        "practice/corporate-governance/",
        CorporateGovernaceView.as_view(),
        name="corporate_governance",
    ),
    path(
        "practice/management/",
        ManagementView.as_view(),
        name="management",
    ),
]
