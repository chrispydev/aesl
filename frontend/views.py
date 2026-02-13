import mimetypes
import os
import json

# from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.generic import DetailView, View
from django.views.generic.list import ListView

from frontend.models import (
    BoardMember,
    Category,
    MainCategory,
    NewsArticle,
    People,
    Project,
    ProjectGalleryImage,
    Publications,
    Staff,
    Branch,
)


class HomeView(View):
    def get(self, request):
        # Fetch all branches for the map
        branches = Branch.objects.all().values(
            "name", "address", "latitude", "longitude", "phone", "email"
        )

        # Convert to JSON-safe list for JavaScript
        branches_json = json.dumps(list(branches))

        # Default center (e.g. Accra) and zoom – will be overridden by fitBounds if branches exist
        default_center = [5.6037, -0.1870]  # Accra coordinates
        default_zoom = 8

        context = {
            "title": "HomePage",
            "branches_json": branches_json,
            "default_center": default_center,
            "default_zoom": default_zoom,
        }
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
        board_members = BoardMember.objects.order_by("-joined_at")
        context = {"title": "Corporate Governance", "board_members": board_members}
        return render(request, "frontend/corporate_governance.html", context)


class BoardMemberView(DetailView):
    model = BoardMember
    template_name = "frontend/board_member.html"
    context_object_name = "board_member"


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


class BoardChairmanView(View):
    def get(self, request):
        context = {"title": "Board Chairman"}
        return render(request, "frontend/board_chairman.html", context)


class ManagingDirectorView(View):
    def get(self, request):
        context = {"title": "Managing Director"}
        return render(request, "frontend/managing_director.html", context)


class DeputyManagingDirectorView(View):
    def get(self, request):
        context = {"title": "Deputy Managing Director"}
        return render(request, "frontend/deputy_managing_director.html", context)


class DeputyIIManagingDirectorView(View):
    def get(self, request):
        context = {"title": "Deputy Managing Director"}
        return render(request, "frontend/deputy_ii_managing_director.html", context)


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
        people = People.objects.all()
        consultants = people.filter(category__iexact="consultants")
        context = {"title": "People", "consultants": consultants}
        return render(request, "frontend/consultants.html", context)


class SeniorProfessionalView(View):
    def get(self, request):
        senior_professionals = People.objects.all()
        context = {"title": "People", "senior_professionals": senior_professionals}
        return render(request, "frontend/senior_professional.html", context)


class AssistantProfessionalsView(View):
    def get(self, request):
        assistant_professionals = People.objects.all()
        context = {
            "title": "People",
            "assistant_professionals": assistant_professionals,
        }
        return render(request, "frontend/assistant_professional.html", context)


class ProfessionalView(View):
    def get(self, request):
        people = People.objects.all()
        professionals = people.filter(category__iexact="professional")
        context = {
            "title": "People",
            "professionals": professionals,
        }
        return render(request, "frontend/professional.html", context)


class SupportTeamView(View):
    def get(self, request):
        people = People.objects.all()
        support_teams = people.filter(category__iexact="support")
        context = {
            "title": "People",
            "support_teams": support_teams,
        }
        return render(request, "frontend/support_team.html", context)


class NationalServiceView(View):
    def get(self, request):
        context = {"title": "People"}
        return render(request, "frontend/national_service.html", context)


class CivicCultureView(View):
    def get(self, request):
        civic_culture_images = ProjectGalleryImage.objects.filter(
            category__iexact="civic",
            is_active=True,  # optional but recommended
        ).order_by("-uploaded_at")  # newest first, or change ordering as you like
        context = {
            "title": "Civic and Culture",
            "civic_culture_images": civic_culture_images,
        }
        return render(request, "frontend/civic_culture.html", context)


class EducationView(View):
    def get(self, request):
        education_images = ProjectGalleryImage.objects.filter(
            category__iexact="education",
            is_active=True,  # optional but recommended
        ).order_by("-uploaded_at")  # newest first, or change ordering as you like

        context = {
            "title": "Education",
            "education_images": education_images,  # better name than just "education"
        }
        return render(request, "frontend/education.html", context)


class HealthView(View):
    def get(self, request):
        health_images = ProjectGalleryImage.objects.filter(
            category__iexact="health",
            is_active=True,  # optional but recommended
        ).order_by("-uploaded_at")  # newest first, or change ordering as you like

        context = {"title": "Health", "health_images": health_images}
        return render(request, "frontend/health.html", context)


class OfficeRetailView(View):
    def get(self, request):
        office_retail_images = ProjectGalleryImage.objects.filter(
            category__iexact="office",
            is_active=True,  # optional but recommended
        ).order_by("-uploaded_at")  # newest first, or change ordering as you like
        context = {
            "title": "Office Retail",
            "office_retail_images": office_retail_images,
        }
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


class PublicationTypeView(View):
    def get(self, request, pub_type):
        # If the type doesn't exist, you can optionally show empty or 404
        publications = Publications.objects.filter(
            type__icontains=pub_type.split("-", 1)[0]
        )

        context = {
            "publications": publications,
            "type": pub_type.rsplit("-", 1)[0].strip(),
            "slug": pub_type,
        }

        return render(request, "frontend/publications_by_type.html", context)


class RightToInformationView(View):
    def get(self, request):
        context = {"title": "Publication"}
        return render(request, "frontend/right_to_information.html", context)


class NewsListView(ListView):
    """
    Displays a paginated list of published news articles
    """

    model = NewsArticle
    template_name = "frontend/news.html"
    context_object_name = "articles"
    paginate_by = 10  # articles per page - adjust as needed

    def get_queryset(self):
        # Only show published articles, ordered by publish date (newest first)
        return (
            NewsArticle.objects.filter(
                is_published=True, publish_date__lte=timezone.now()
            )
            .select_related("category", "author")
            .order_by("-publish_date")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add featured articles (optional)
        context["featured_articles"] = NewsArticle.objects.filter(
            is_published=True, is_featured=True, publish_date__lte=timezone.now()
        ).order_by("-publish_date")[:3]

        # Add all active categories for sidebar/filter
        context["categories"] = Category.objects.filter(is_active=True)

        return context


class NewsDetailView(DetailView):
    """
    Displays a single news article
    """

    model = NewsArticle
    template_name = "frontend/news_detail.html"
    context_object_name = "article"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        # Only allow access to published articles
        return NewsArticle.objects.filter(
            is_published=True, publish_date__lte=timezone.now()
        ).select_related("category", "author")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Increment views count (simple version)
        self.object.views_count += 1
        self.object.save(update_fields=["views_count"])

        # Related articles (same category, exclude current)
        context["related_articles"] = (
            NewsArticle.objects.filter(
                category=self.object.category,
                is_published=True,
                publish_date__lte=timezone.now(),
            )
            .exclude(id=self.object.id)
            .order_by("-publish_date")[:4]
        )

        # Gallery images
        context["gallery_images"] = self.object.images.all().order_by("order")

        # All categories for sidebar
        context["categories"] = Category.objects.filter(is_active=True)

        return context


class CategoryNewsListView(ListView):
    """
    Displays news articles filtered by category
    """

    model = NewsArticle
    template_name = "news_list.html"  # reuse the same template
    context_object_name = "articles"
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(
            Category, slug=self.kwargs.get("slug"), is_active=True
        )

        return (
            NewsArticle.objects.filter(
                category=self.category,
                is_published=True,
                publish_date__lte=timezone.now(),
            )
            .select_related("category", "author")
            .order_by("-publish_date")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_category"] = self.category
        context["categories"] = Category.objects.filter(is_active=True)
        context["page_title"] = f"{self.category.name} - News"
        return context
