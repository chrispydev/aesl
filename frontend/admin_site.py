"""Branded Django admin site for the AESL engineering content dashboard.

The stock ``admin.site`` is intentionally left alone. All AESL models are
registered against :data:`admin_site` and ``aesl/urls.py`` mounts that site at
``/admin/`` so the dashboard can provide extra context (live content metrics)
without touching Django internals.
"""

from django.contrib.admin import AdminSite
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User
from django.utils import timezone

from .models import (
    Alumni,
    BoardMember,
    Branch,
    NewsArticle,
    People,
    Project,
    ProjectGalleryImage,
    Publications,
    Staff,
)


class AESLAdminSite(AdminSite):
    """Admin site with AESL branding and a data-driven overview page."""

    site_title = "AESL Control Center"
    site_header = "AESL Control Center"
    index_title = "Overview"
    site_url = "/"

    def each_context(self, request):
        context = super().each_context(request)
        context["aesl_brand"] = "AESL"
        return context

    def index(self, request, extra_context=None):
        extra_context = dict(extra_context or {})
        extra_context["aesl_metrics"] = self.get_content_metrics()
        return super().index(request, extra_context)

    @staticmethod
    def _count(manager, **filters):
        """Count rows without ever breaking the admin if a table is missing."""
        try:
            if filters:
                return manager.filter(**filters).count()
            return manager.count()
        except Exception:
            return 0

    @classmethod
    def get_content_metrics(cls):
        now = timezone.now()
        projects = Project.objects
        articles = NewsArticle.objects

        return {
            "projects": {
                "total": cls._count(projects),
                "ongoing": cls._count(projects, completed_date__isnull=True),
                "completed": cls._count(projects, completed_date__isnull=False),
            },
            "news": {
                "total": cls._count(articles),
                "published": cls._count(
                    articles, is_published=True, publish_date__lte=now
                ),
                "drafts": cls._count(articles, is_published=False),
                "featured": cls._count(articles, is_featured=True),
            },
            "team": {
                "staff": cls._count(Staff.objects),
                "people": cls._count(People.objects),
                "board": cls._count(BoardMember.objects),
                "alumni": cls._count(Alumni.objects),
            },
            "library": {
                "publications": cls._count(Publications.objects),
                "gallery": cls._count(ProjectGalleryImage.objects, is_active=True),
                "branches": cls._count(Branch.objects),
            },
        }


admin_site = AESLAdminSite(name="admin")


def register(*models):
    """Decorator equivalent of ``django.contrib.admin.register`` for our site.

    ``AdminSite.register()`` is a plain method that returns None, so it cannot
    be used directly as a decorator. This wrapper registers the admin class
    and returns it, exactly like Django's own decorator does.
    """
    def decorator(admin_class):
        admin_site.register(models, admin_class=admin_class)
        return admin_class
    return decorator


# Django's auth app registers these on the default site only, so add them here.
admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)
