from django.views import View
from django.shortcuts import render
from django.views.generic import DetailView

from frontend.models import Project


class HomeView(View):
    def get(self, request):
        context = {"title": "HomePage"}
        return render(request, "frontend/home.html", context)


class ProjectView(View):
    def get(self, request):
        projects = Project.objects.all()
        context = {"title": "Projects", "projects": projects}
        return render(request, "frontend/projects.html", context)


class PracticeView(View):
    def get(self, request):
        context = {"title": "Practice"}
        return render(request, "frontend/practice.html", context)


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
