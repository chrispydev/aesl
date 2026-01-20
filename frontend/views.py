import mimetypes
import os

# from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, View

from frontend.models import MainCategory, Project, Publications, Staff


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
        context["project_3d_visualization_picture"] = project.gallery.filter(
            image_type="project_3d_visualizations"
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
        context = {"title": "Sector Ministry"}
        return render(request, "frontend/sector_ministry.html", context)


class CorporateGovernaceView(View):
    def get(self, request):
        context = {"title": "Practice"}
        return render(request, "frontend/corporate_governance.html", context)


class BoardChairmanView(View):
    def get(self, request):
        context = {"title": "Board Chairman"}
        return render(request, "frontend/board_chairman.html", context)


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


class PrincipalConsultantsView(View):
    def get(self, request):
        context = {"title": "People"}
        return render(request, "frontend/principal__consultants.html", context)


class SeniorConsultantsView(View):
    def get(self, request):
        context = {"title": "People"}
        return render(request, "frontend/senior_consultants.html", context)


class ConsultantsView(View):
    def get(self, request):
        context = {"title": "People"}
        return render(request, "frontend/consultants.html", context)


class SeniorProfessionalView(View):
    def get(self, request):
        context = {"title": "People"}
        return render(request, "frontend/senior_professional.html", context)


class AssistantProfessionalsView(View):
    def get(self, request):
        context = {"title": "People"}
        return render(request, "frontend/assistant_professional.html", context)


class ProfessionalView(View):
    def get(self, request):
        context = {"title": "People"}
        return render(request, "frontend/professional.html", context)


class SupportTeamView(View):
    def get(self, request):
        context = {"title": "People"}
        return render(request, "frontend/support_team.html", context)


class NationalServiceView(View):
    def get(self, request):
        context = {"title": "People"}
        return render(request, "frontend/national_service.html", context)


class PublicationsView(View):
    def get(self, request):
        publications = Publications.objects.all()
        context = {"title": "Publication", "publications": publications}
        return render(request, "frontend/publications.html", context)


class PublicationDownloadView(View):
    def get(self, request, pk):
        publication = get_object_or_404(Publications, pk=pk)

        if not publication.download:
            raise Http404("File not found")

        file_path = publication.download.path

        if not os.path.exists(file_path):
            raise Http404("File not found")

        # Get the mime type
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is None:
            mime_type = "application/octet-stream"

        # Open and read the file
        with open(file_path, "rb") as file:
            response = HttpResponse(file.read(), content_type=mime_type)

        # Set the filename for download
        filename = os.path.basename(file_path)
        response["Content-Disposition"] = f'attachment; filename="{filename}"'

        return response


class CivicCultureView(View):
    def get(self, request):
        context = {"title": "Civic Culture"}
        return render(request, "frontend/civic_culture.html", context)


class EducationView(View):
    def get(self, request):
        context = {"title": "Education"}
        return render(request, "frontend/education.html", context)


class HealthView(View):
    def get(self, request):
        context = {"title": "Health"}
        return render(request, "frontend/health.html", context)


class OfficeRetailView(View):
    def get(self, request):
        context = {"title": "Office Retail"}
        return render(request, "frontend/office_retail.html", context)


class ResidentialView(View):
    def get(self, request):
        context = {"title": "Residential"}
        return render(request, "frontend/residential.html", context)


class IndustrialInfrastructureView(View):
    def get(self, request):
        context = {"title": "Industrial Infrastructure"}
        return render(request, "frontend/industrial_infrastructure.html", context)


class HospitalityView(View):
    def get(self, request):
        context = {"title": "Hospitality"}
        return render(request, "frontend/hospitality.html", context)


class SportLesisureView(View):
    def get(self, request):
        context = {"title": "Sport and Leisure"}
        return render(request, "frontend/sport_leisure.html", context)


class LandScapePlanningView(View):
    def get(self, request):
        context = {"title": "Landscaping and Planning"}
        return render(request, "frontend/landscaping_planning.html", context)


class ProjectListView(View):
    def get(self, request):
        projects = Project.objects.all()
        context = {"title": "Projects List", "projects": projects}
        return render(request, "frontend/project_list.html", context)
