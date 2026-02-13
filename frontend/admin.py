from django.contrib import admin
from django.utils.html import format_html

from .models import (
    BoardMember,
    Branch,
    Category,
    ContractorRole,
    ExternalAuthor,
    MainCategory,
    NewsArticle,
    NewsImage,
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
        "position",
        "profession",
        "email",
        "sub_category",
    )

    list_filter = ("sub_category", "position")
    search_fields = ("name", "email", "position", "profession")


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
        "joined_at",
    )
    list_editable = ("joined_at",)
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


class NewsImageInline(admin.TabularInline):
    """
    Inline for managing multiple images attached to a news article.
    """

    model = NewsImage
    extra = 1
    fields = ("image", "caption", "order")
    readonly_fields = ("preview",)

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{url}" style="max-height: 100px; border-radius: 4px;" />',
                url=obj.image.url,
            )
        return "-"

    preview.short_description = "Preview"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for news categories.
    """

    list_display = ("name", "slug", "article_count", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)

    fieldsets = (
        (None, {"fields": ("name", "slug", "description", "is_active")}),
        (("Timestamps"), {"fields": ("created_at",), "classes": ("collapse",)}),
    )
    readonly_fields = ("created_at",)

    def article_count(self, obj):
        return obj.articles.count()

    article_count.short_description = "Articles"


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    """
    Professional admin interface for news articles.
    """

    list_display = (
        "title",
        "category_link",
        "is_published",
        "publish_date",
        "author",
        "is_featured",
        "views_count",
    )
    list_filter = (
        "is_published",
        "is_featured",
        "category",
        "publish_date",
        "author",
    )
    list_editable = ("is_published", "is_featured")
    search_fields = ("title", "excerpt", "content", "tags")
    date_hierarchy = "publish_date"
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at", "views_count")
    inlines = [NewsImageInline]

    fieldsets = (
        (
            ("Basic Information"),
            {
                "fields": (
                    "title",
                    "slug",
                    "category",
                    "author",
                    "featured_image",
                )
            },
        ),
        (
            ("Content"),
            {
                "fields": (
                    "excerpt",
                    "content",
                    "tags",
                )
            },
        ),
        (
            ("Publishing"),
            {
                "fields": (
                    "is_published",
                    "publish_date",
                    "is_featured",
                )
            },
        ),
        (
            ("SEO"),
            {
                "fields": (
                    "meta_title",
                    "meta_description",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            ("Statistics"),
            {
                "fields": ("views_count", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def category_link(self, obj):
        if obj.category:
            url = f"/admin/news/category/{obj.category.id}/change/"
            return format_html('<a href="{}">{}</a>', url, obj.category.name)
        return "-"

    category_link.short_description = "Category"

    # Optional: custom actions
    actions = ["make_published", "make_unpublished"]

    @admin.action(description=("Mark selected articles as published"))
    def make_published(self, request, queryset):
        queryset.update(is_published=True)

    @admin.action(description=("Mark selected articles as draft (unpublished)"))
    def make_unpublished(self, request, queryset):
        queryset.update(is_published=False)


@admin.register(NewsImage)
class NewsImageAdmin(admin.ModelAdmin):
    """
    Standalone admin for news gallery images (optional).
    """

    list_display = ("article_title", "preview", "caption", "order")
    list_filter = ("article__category",)
    search_fields = ("article__title", "caption")
    readonly_fields = ("preview",)

    def article_title(self, obj):
        return obj.article.title

    article_title.short_description = "Article"

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{url}" style="max-height: 80px; border-radius: 4px;" />',
                url=obj.image.url,
            )
        return "-"

    preview.short_description = "Preview"


@admin.register(ExternalAuthor)
class ExternalAuthorAdmin(admin.ModelAdmin):
    """
    Admin for external authors (if used).
    """

    list_display = ("name", "title", "preview_photo")
    search_fields = ("name", "title", "bio")
    readonly_fields = ("preview_photo",)

    def preview_photo(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{url}" style="max-height: 60px; border-radius: 50%;" />',
                url=obj.photo.url,
            )
        return "-"

    preview_photo.short_description = "Photo"


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "address_short",
        "location_link",
        "phone",
        "email",
        "created_at",
    )
    list_filter = ("created_at",)
    search_fields = ("name", "address", "phone", "email")
    readonly_fields = (
        "created_at",
        "map_preview",
    )  # ← this is allowed for custom methods
    list_per_page = 20

    fieldsets = (
        (
            ("Branch Information"),
            {
                "fields": (
                    "name",
                    "address",
                    "phone",
                    "email",
                )
            },
        ),
        (
            ("Geolocation"),
            {
                "fields": (
                    "latitude",
                    "longitude",
                ),
                "description": (
                    "Enter latitude and longitude in decimal degrees (e.g. Accra ≈ 5.6037, -0.1870)"
                ),
            },
        ),
        (
            ("Map Preview"),
            {
                "fields": ("map_preview",),
                "classes": ("collapse",),  # collapsed by default
                "description": ("Live preview of the location on OpenStreetMap"),
            },
        ),
        (
            ("Metadata"),
            {
                "fields": ("created_at",),
                "classes": ("collapse",),
            },
        ),
    )

    # Custom display methods (no underscores in names to avoid confusion)
    @admin.display(description=("Short Address"))
    def address_short(self, obj):
        return obj.address[:60] + "..." if len(obj.address) > 60 else obj.address

    @admin.display(description=("Coordinates"))
    def location_link(self, obj):
        if obj.latitude is not None and obj.longitude is not None:
            url = f"https://www.openstreetmap.org/?mlat={obj.latitude}&mlon={obj.longitude}#map=15/{obj.latitude}/{obj.longitude}"
            # Format numbers manually (no :.5f inside format_html)
            lat_str = f"{float(obj.latitude):.5f}"
            lon_str = f"{float(obj.longitude):.5f}"
            return format_html(
                '<a href="{}" target="_blank" rel="noopener">{}, {}</a>',
                url,
                lat_str,
                lon_str,
            )
        return "—"

    @admin.display(description=("Map Preview"))
    def map_preview(self, obj):
        if obj.latitude is None or obj.longitude is None:
            return "No coordinates provided — save the branch first to see preview"

        embed_url = (
            f"https://www.openstreetmap.org/export/embed.html?"
            f"bbox={obj.longitude - 0.03},{obj.latitude - 0.03},"
            f"{obj.longitude + 0.03},{obj.latitude + 0.03}&"
            f"layer=mapnik&marker={obj.latitude},{obj.longitude}"
        )

        return format_html(
            '<iframe width="100%" height="350" frameborder="0" scrolling="no" '
            f'marginheight="0" marginwidth="0" src="{embed_url}"></iframe>'
            "<br><small>"
            f'<a href="https://www.openstreetmap.org/?mlat={obj.latitude}&mlon={obj.longitude}#map=16/{obj.latitude}/{obj.longitude}" '
            'target="_blank" rel="noopener">View larger map on OpenStreetMap →</a></small>'
        )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["latitude"].help_text = "Example for Accra: 5.6037"
        form.base_fields["longitude"].help_text = "Example for Accra: -0.1870"
        return form
