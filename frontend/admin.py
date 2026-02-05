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


class PublicationsInline(admin.TabularInline):
    model = Publications
    extra = 1
    fields = ("title", "type", "author", "download", "publication_image_preview")

    # Optional: small preview in inline too
    readonly_fields = ("publication_image_preview",)

    def publication_image_preview(self, obj):
        if obj.publication_image:
            return format_html(
                '<img src="{}" style="max-height: 60px; border-radius: 4px; object-fit: cover;">',
                obj.publication_image.url,
            )
        return "No image"

    publication_image_preview.short_description = "Preview"


@admin.register(Publications)
class PublicationsAdmin(admin.ModelAdmin):
    list_display = (
        "thumbnail_preview",  # ← small thumbnail column
        "title",
        "type",
        "author",
        "download",
    )
    list_display_links = ("title",)  # make title clickable
    search_fields = ("title", "type", "author")
    ordering = ("-title",)
    list_per_page = 20

    readonly_fields = ("large_preview",)  # large image preview in form

    fieldsets = (
        (
            "Publication Info",
            {
                "fields": (
                    "title",
                    "type",
                    "author",
                    "download",
                ),
            },
        ),
        (
            "Image",
            {
                "fields": (
                    "publication_image",
                    "large_preview",
                ),
            },
        ),
    )

    # Small thumbnail in list view
    def thumbnail_preview(self, obj):
        if obj.publication_image:
            return format_html(
                '<img src="{}" style="max-height: 60px; border-radius: 6px; object-fit: cover;">',
                obj.publication_image.url,
            )
        return format_html('<span style="color: #999;">No image</span>')

    thumbnail_preview.short_description = "Image"

    # Larger preview in change form
    def large_preview(self, obj):
        if obj.publication_image:
            return format_html(
                '<img src="{}" style="max-height: 300px; max-width: 100%; border-radius: 8px; border: 1px solid #ddd;">',
                obj.publication_image.url,
            )
        return format_html('<p style="color: #666;">No image uploaded</p>')

    large_preview.short_description = "Image Preview"


@admin.register(BoardMember)
class BoardMemberAdmin(admin.ModelAdmin):
    list_display = (
        "thumbnail_preview",  # ← new: shows small image thumbnail
        "name",
        "position",
    )
    list_display_links = ("name",)  # make name clickable to edit
    search_fields = ("name", "position", "about")

    list_per_page = 20  # optional: more items per page

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "name",
                    "position",
                    "image",
                    "thumbnail_large",  # ← new: large preview in edit form
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

    readonly_fields = ("thumbnail_large",)  # ← make preview read-only

    # === Small thumbnail in list view ===
    def thumbnail_preview(self, obj):
        if obj.image and obj.image.url:
            return format_html(
                '<img src="{}" style="max-height: 60px; border-radius: 6px; object-fit: cover;">',
                obj.image.url,
            )
        return format_html(
            '<span style="color: #999; font-style: italic;">No image</span>'
        )

    thumbnail_preview.short_description = "Photo"

    # === Larger preview in change/edit form ===
    def thumbnail_large(self, obj):
        if obj.image and obj.image.url:
            return format_html(
                '<img src="{}" style="max-height: 300px; max-width: 100%; border-radius: 8px; border: 1px solid #ddd; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">',
                obj.image.url,
            )
        return format_html(
            '<p style="color: #666; font-style: italic;">No photo uploaded yet</p>'
        )

    thumbnail_large.short_description = "Photo Preview"


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
