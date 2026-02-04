from django.contrib import admin
from django.utils.html import format_html

from .models import (
    BoardMember,
    ContractorRole,
    MainCategory,
    People,
    Project,
    ProjectAward,
    ProjectCategory,
    ProjectContractor,
    ProjectGalleryImage,
    ProjectImage,
    ProjectLeader,
    ProjectTeamMember,
    Publications,
    Staff,
    SubCategory,
)

# ==================================================
# INLINE MODELS
# ==================================================


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ("image", "image_type")


class ProjectAwardInline(admin.TabularInline):
    model = ProjectAward
    extra = 1
    fields = ("year", "award_name", "awarded_by", "website")
    ordering = ("-year",)


class ProjectContractorInline(admin.TabularInline):
    model = ProjectContractor
    extra = 1


class StaffInline(admin.TabularInline):
    model = Staff
    extra = 1
    fields = ("name", "image", "grade", "region", "email", "description")


class PublicationsInline(admin.TabularInline):
    model = Publications
    extra = 1
    fields = ("title", "type", "author", "download")


# ==================================================
# PROJECT ADMIN
# ==================================================


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
        "other_team_members__full_name",
    )

    filter_horizontal = (
        "project_leaders",
        "other_team_members",
    )

    inlines = [
        ProjectImageInline,
        ProjectAwardInline,
        ProjectContractorInline,
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
        return obj.start_date.strftime("%B %Y") if obj.start_date else "-"

    formatted_start_date.short_description = "Start Date"
    formatted_start_date.admin_order_field = "start_date"

    def formatted_completed_date(self, obj):
        if obj.completed_date:
            return obj.completed_date.strftime("%B %Y")
        return format_html(
            '<span style="color:#8a1f1f;font-weight:500;">{}</span>',
            "Still in Progress",
        )

    # def formatted_completed_date(self, obj):
    #     if obj.completed_date:
    #         return obj.completed_date.strftime("%B %Y")
    #     return format_html(
    #         '<span style="color:#8a1f1f;font-weight:500;">Still in Progress</span>'
    #     )

    formatted_completed_date.short_description = "Completed Date"
    formatted_completed_date.admin_order_field = "completed_date"


# ==================================================
# SUPPORTING ADMINS
# ==================================================


@admin.register(ProjectAward)
class ProjectAwardAdmin(admin.ModelAdmin):
    list_display = ("year", "award_name", "awarded_by", "project")
    list_filter = ("year",)
    search_fields = ("award_name", "awarded_by", "project__title")
    ordering = ("-year",)


@admin.register(ProjectContractor)
class ProjectContractorAdmin(admin.ModelAdmin):
    list_display = ("project", "role", "company_name")
    list_filter = ("role",)
    search_fields = ("company_name", "project__title")


@admin.register(ContractorRole)
class ContractorRoleAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(ProjectLeader)
class ProjectLeaderAdmin(admin.ModelAdmin):
    search_fields = ("full_name",)


@admin.register(ProjectTeamMember)
class ProjectTeamMemberAdmin(admin.ModelAdmin):
    search_fields = ("full_name",)


@admin.register(MainCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "main_category")
    list_filter = ("main_category",)
    search_fields = ("name",)

    inlines = [StaffInline]


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "grade",
        "email",
        "sub_category",
    )

    list_filter = ("sub_category", "grade")
    search_fields = ("name", "email", "grade")


@admin.register(People)
class PeopleAdmin(admin.ModelAdmin):
    list_display = ("name", "profession")
    search_fields = ("name", "profession")


@admin.register(Publications)
class PublicationsAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "author", "download", "publication_image")
    search_fields = ("title", "type", "author")
    ordering = ("-title",)


@admin.register(BoardMember)
class BoardMemberAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "name",
                    "position",
                    "image",
                    "about",
                )
            },
        ),
        (
            "Social Media",
            {
                "fields": (
                    "linkedin",
                    "twitter",
                )
            },
        ),
    )


@admin.register(ProjectGalleryImage)
class ProjectGalleryImageAdmin(admin.ModelAdmin):
    list_display = [
        "thumbnail",
        "alt_text_short",
        "category",
        "uploaded_at",
        "is_active",
    ]

    list_display_links = ["alt_text_short"]

    list_filter = [
        "category",
        "is_active",
        "uploaded_at",
    ]

    search_fields = [
        "alt_text",
        "category",
    ]

    readonly_fields = ["thumbnail_preview", "uploaded_at"]

    fieldsets = (
        (
            "Image",
            {
                "fields": ("image", "thumbnail_preview"),
                "classes": ("wide",),
            },
        ),
        (
            "Metadata",
            {
                "fields": ("alt_text", "category", "is_active"),
            },
        ),
        (
            "System Info",
            {
                "fields": ("uploaded_at",),
                "classes": ("collapse",),
            },
        ),
    )

    # Show small thumbnail in list view
    def thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 60px; border-radius: 4px;">',
                obj.image.url,
            )
        return "-"

    thumbnail.short_description = "Preview"

    # Larger preview in change form
    def thumbnail_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 300px; max-width: 100%; border: 1px solid #ddd; border-radius: 6px;">',
                obj.image.url,
            )
        return "No image uploaded yet"

    thumbnail_preview.short_description = "Image Preview"

    # Shortened alt text for list view
    def alt_text_short(self, obj):
        return obj.alt_text[:60] + "..." if len(obj.alt_text) > 60 else obj.alt_text

    alt_text_short.short_description = "Alt Text"

    # Make list view nicer
    list_per_page = 20
