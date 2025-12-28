from django.urls import path
from frontend.views import (
    CorporateGovernaceView,
    EngineeringView,
    FunctionsView,
    HistoryView,
    HomeView,
    ManagementView,
    ManagingDirectorView,
    MandateView,
    MissionVisionView,
    PracticeView,
    ProjectDetailView,
    ProjectView,
    SectorMinistryView,
    StaffDetailView,
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
    path(
        "practice/management/<int:pk>/", StaffDetailView.as_view(), name="staff_detail"
    ),
    path(
        "practice/management/managing-director/",
        ManagingDirectorView.as_view(),
        name="managing_director",
    ),
    path(
        "practice/management/deputy-managing-director/engineering/",
        EngineeringView.as_view(),
        name="engineering",
    ),
    path(
        "practice/history/",
        HistoryView.as_view(),
        name="history",
    ),
    path(
        "practice/functions/",
        FunctionsView.as_view(),
        name="functions",
    ),
    path(
        "practice/mandate/",
        MandateView.as_view(),
        name="mandate",
    ),
    path(
        "practice/mission-vision-and-values/",
        MissionVisionView.as_view(),
        name="mission_vision",
    ),
]
