from django.shortcuts import render
from django.views.generic import DetailView, View

from frontend.models import MainCategory, Project, Staff


class HomeView(View):
    def get(self, request):
        context = {"title": "HomePage"}
        return render(request, "frontend/home.html", context)


class ProjectView(View):
    def get(self, request):
        projects = Project.objects.all()
        context = {"title": "Projects", "projects": projects}
        return render(request, "frontend/projects.html", context)


class ProjectDetailView(DetailView):
    model = Project
    template_name = "frontend/project_detail.html"
    context_object_name = "project"  # Default is 'object', but we can use 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()

        # Separate gallery images
        context["project_pictures"] = project.gallery.filter(image_type="project")
        context["construction_pictures"] = project.gallery.filter(
            image_type="construction"
        )
        # current page location
        context["title"] = "Projects"

        return context


class PracticeView(View):
    def get(self, request):
        context = {"title": "Practice"}
        return render(request, "frontend/practice.html", context)


class SectorMinistryView(View):
    def get(self, request):
        context = {"title": "Sector Ministr"}
        return render(request, "frontend/sector_ministry.html", context)


class CorporateGovernaceView(View):
    def get(self, request):
        context = {"title": "Practice"}
        return render(request, "frontend/corporate_governance.html", context)


class ManagementView(View):
    def get(self, request):
        categories = MainCategory.objects.prefetch_related("sub_categories__staff")

        context = {
            "title": "Management",
            "categories": categories,
        }
        return render(request, "frontend/management.html", context)


class StaffDetailView(DetailView):
    model = Staff
    template_name = "frontend/staff_detail.html"
    context_object_name = "staff"


class ManagingDirectorView(View):
    def get(self, request):
        context = {"title": "Managing Director"}
        return render(request, "frontend/managing_director.html", context)


class EngineeringView(View):
    def get(self, request):
        context = {"title": "Deputy Managing Director - Engineering"}
        return render(request, "frontend/engineering.html", context)


class HistoryView(View):
    def get(self, request):
        context = {"title": "History"}
        return render(request, "frontend/history.html", context)


class FunctionsView(View):
    def get(self, request):
        context = {"title": "Functions"}
        return render(request, "frontend/functions.html", context)


class MandateView(View):
    def get(self, request):
        context = {"title": "Mandate"}
        return render(request, "frontend/mandate.html", context)


class MissionVisionView(View):
    def get(self, request):
        context = {"title": "Mission, Vision & Values"}
        return render(request, "frontend/mission_vision.html", context)


class ServiceView(View):
    def get(self, request):
        context = {"title": "Services"}
        return render(request, "frontend/services.html", context)


class PrinciplesView(View):
    def get(self, request):
        context = {"title": "Principles"}
        return render(request, "frontend/principles.html", context)


class PeopleView(View):
    def get(self, request):
        context = {"title": "People"}
        return render(request, "frontend/people.html", context)
