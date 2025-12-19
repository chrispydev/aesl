from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Project,
    ProjectCategory,
    ProjectLeader,
    ProjectImage,
    ProjectAward,
    ProjectTeamMember,
)


# -----------------------------
# PROJECT IMAGE INLINE
# -----------------------------
class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ("image", "image_type")


# -----------------------------
# PROJECT AWARD INLINE (NEW)
# -----------------------------
class ProjectAwardInline(admin.TabularInline):
    model = ProjectAward
    extra = 1
    fields = ("year", "award_name", "awarded_by", "website")
    ordering = ("-year",)


# -----------------------------
# PROJECT ADMIN
# -----------------------------
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "client",
        "location",
        "category",
        "formatted_start_date",
        "formatted_completed_date",
    )

    list_filter = ("category",)
    search_fields = (
        "title",
        "client",
        "location",
        "project_coordinator",
        "project_leaders__full_name",
        "other_team_members__full_name",  # ✅ NEW
    )

    filter_horizontal = (
        "project_leaders",
        "other_team_members",
    )

    # ✅ CONNECTED HERE
    inlines = [
        ProjectImageInline,
        ProjectAwardInline,
    ]

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "title",
                    "client",
                    "location",
                    "category",
                    "picture",
                    "little_text_details",
                )
            },
        ),
        (
            "Team",
            {
                "fields": (
                    "project_coordinator",
                    "project_leaders",
                    "other_team_members",
                )
            },
        ),
        (
            "Project Details",
            {
                "fields": (
                    "total_floor_area",
                    "start_date",
                    "completed_date",
                )
            },
        ),
        (
            "Documentation",
            {
                "fields": (
                    "job_sheets",
                    "certificate",
                )
            },
        ),
    )

    # -----------------------------
    # CUSTOM DATE DISPLAY
    # -----------------------------
    def formatted_start_date(self, obj):
        if obj.start_date:
            return obj.start_date.strftime("%B %Y")
        return "-"

    formatted_start_date.short_description = "Start Date"
    formatted_start_date.admin_order_field = "start_date"

    def formatted_completed_date(self, obj):
        if obj.completed_date:
            return obj.completed_date.strftime("%B %Y")

        return format_html(
            '<span style="color:#8a1f1f;font-weight:500;">{}</span>',
            "Still in Progress",
        )

    formatted_completed_date.short_description = "Completed Date"
    formatted_completed_date.admin_order_field = "completed_date"


# -----------------------------
# PROJECT AWARD ADMIN (OPTIONAL BUT RECOMMENDED)
# -----------------------------
@admin.register(ProjectAward)
class ProjectAwardAdmin(admin.ModelAdmin):
    list_display = ("year", "award_name", "awarded_by", "project")
    list_filter = ("year",)
    search_fields = ("award_name", "awarded_by", "project__title")
    ordering = ("-year",)


# -----------------------------
# CATEGORY ADMIN
# -----------------------------
@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


# -----------------------------
# PROJECT LEADER ADMIN
# -----------------------------
@admin.register(ProjectLeader)
class ProjectLeaderAdmin(admin.ModelAdmin):
    search_fields = ("full_name",)


# -----------------------------
# PROJECT OTHER TEAM MEMBERS
# -----------------------------
@admin.register(ProjectTeamMember)
class ProjectTeamMemberAdmin(admin.ModelAdmin):
    search_fields = ("full_name",)
