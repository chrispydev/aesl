import os
from io import BytesIO
from unicodedata import category
from django.contrib.auth.models import User
from django.utils import timezone

from django.core.files.base import ContentFile
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from PIL import Image


# ==============================
# IMAGE OPTIMIZATION MIXIN
# ==============================
class ImageOptimizeMixin:
    IMAGE_MAX_SIZE = (1200, 1200)
    IMAGE_QUALITY = 85

    def optimize_image(self, image_field):
        if not image_field:
            return

        img = Image.open(image_field)

        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        img.thumbnail(self.IMAGE_MAX_SIZE, Image.LANCZOS)

        ext = os.path.splitext(image_field.name)[1].lower()
        buffer = BytesIO()

        if ext in [".jpg", ".jpeg"]:
            img.save(buffer, format="JPEG", quality=self.IMAGE_QUALITY, optimize=True)
        elif ext == ".png":
            img.save(buffer, format="PNG", optimize=True)
        elif ext == ".webp":
            img.save(buffer, format="WEBP", quality=self.IMAGE_QUALITY)
        else:
            img.save(buffer)

        buffer.seek(0)
        image_field.save(image_field.name, ContentFile(buffer.read()), save=False)


# ==============================
# PROJECT MODELS
# ==============================
class ProjectCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProjectLeader(models.Model):
    full_name = models.CharField(max_length=150)

    def __str__(self):
        return self.full_name


class ProjectTeamMember(models.Model):
    full_name = models.CharField(max_length=150)

    def __str__(self):
        return self.full_name


class Project(models.Model, ImageOptimizeMixin):
    title = models.CharField(max_length=200)
    client = models.CharField(max_length=200)
    location = models.CharField(max_length=300, default="Accra")

    picture = models.ImageField(
        upload_to="projects/main_pictures/", blank=True, null=True
    )

    little_text_details = models.TextField()
    project_coordinator = models.CharField(max_length=150)

    project_leaders = models.ManyToManyField(ProjectLeader, related_name="projects")
    other_team_members = models.ManyToManyField(
        ProjectTeamMember, related_name="projects", blank=True
    )

    total_floor_area = models.CharField(max_length=100)
    start_date = models.DateField()
    completed_date = models.DateField(blank=True, null=True)

    job_sheets = models.CharField(max_length=300, blank=True)
    certificate = models.CharField(max_length=300, blank=True)

    category = models.ForeignKey(
        ProjectCategory, on_delete=models.SET_NULL, null=True, related_name="projects"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.picture:
            self.optimize_image(self.picture)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ProjectAward(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="awards"
    )
    year = models.PositiveIntegerField()
    award_name = models.CharField(max_length=200)
    awarded_by = models.CharField(max_length=200)
    website = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-year", "award_name"]

    def __str__(self):
        return f"{self.year} - {self.award_name}"


class ProjectImage(models.Model, ImageOptimizeMixin):
    PROJECT_PICTURE = "project"
    CONSTRUCTION_PICTURE = "construction"
    PROJECT_3D_VISUALIZATIONS_PICTURE = "project_3d_visualizations"

    IMAGE_TYPE_CHOICES = [
        (PROJECT_PICTURE, "Project Pictures"),
        (CONSTRUCTION_PICTURE, "Construction Pictures"),
        (PROJECT_3D_VISUALIZATIONS_PICTURE, "Project 3D Visualizations"),
    ]

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="gallery"
    )
    image = models.ImageField(upload_to="projects/gallery/")
    image_type = models.CharField(max_length=30, choices=IMAGE_TYPE_CHOICES)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.image:
            self.optimize_image(self.image)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.project.title} - {self.image_type}"


class ProjectGalleryImage(models.Model):
    image = models.ImageField(
        upload_to="projects-gallery/",
        verbose_name="Gallery Image",
        help_text="Upload the main image for the gallery",
        max_length=350,
    )

    category = models.CharField(
        max_length=100,
        verbose_name="Category",
        help_text="e.g. Education, Sport and Leisure, Culture, etc.",
        blank=True,
        db_index=True,  # helps with filtering/sorting by category
    )

    alt_text = models.CharField(
        max_length=500,
        verbose_name="Image Alt Text",
        help_text="Descriptive text for accessibility and SEO (screen readers)",
        blank=True,
        unique=True,
    )

    # Optional useful fields (you can remove if not needed)
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Upload Date")
    is_active = models.BooleanField(
        default=True,
        verbose_name="Visible",
        help_text="Uncheck to hide this image without deleting it",
    )

    class Meta:
        verbose_name = "Project Gallery Image"
        verbose_name_plural = "Project Gallery Images"
        ordering = ["-uploaded_at"]  # newest first
        indexes = [
            models.Index(fields=["category"]),
        ]

    def __str__(self):
        # Nice display in admin and shell
        name = self.alt_text or self.category or "Untitled Image"
        return f"{name} ({self.uploaded_at.strftime('%Y-%m-%d')})"

    # Optional: better delete behavior (clean up file)
    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete(save=False)  # delete file from storage
        super().delete(*args, **kwargs)


# ==============================
# CONTRACTORS
# ==============================
class ContractorRole(models.Model):
    name = models.CharField(max_length=150, unique=True)

    class Meta:
        verbose_name = "Contractor Role"
        verbose_name_plural = "Contractor Roles"

    def __str__(self):
        return self.name


class ProjectContractor(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="contractors"
    )
    role = models.ForeignKey(
        ContractorRole, on_delete=models.PROTECT, related_name="project_contractors"
    )
    company_name = models.CharField(max_length=200)

    class Meta:
        unique_together = ("project", "role")
        ordering = ("role__name",)

    def __str__(self):
        return f"{self.role.name} - {self.company_name}"


# ==============================
# STAFF
# ==============================
class MainCategory(models.Model):
    name = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural = "Main Categories"

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    main_category = models.ForeignKey(
        MainCategory, on_delete=models.CASCADE, related_name="sub_categories"
    )
    name = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural = "Sub Categories"

    def __str__(self):
        return f"{self.main_category} - {self.name}"


class Staff(models.Model, ImageOptimizeMixin):
    sub_category = models.ForeignKey(
        SubCategory, on_delete=models.CASCADE, related_name="staff"
    )
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to="staff_images/", blank=True, null=True)
    position = models.CharField(max_length=100)
    region = models.CharField(max_length=100, default="Not a Regional Head")
    profession = models.CharField(max_length=100, default="Surveying")
    email = models.EmailField()
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if self.image:
            self.optimize_image(self.image)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# ==============================
# PEOPLE
# ==============================
class People(models.Model, ImageOptimizeMixin):
    name = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to="people/", blank=True, null=True)
    position = models.CharField(max_length=100, default="position", blank=True)
    category = models.CharField(max_length=100, default="category")
    department = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)
    profession = models.CharField(max_length=100, default="Surveying")

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.profile_picture:
            self.optimize_image(self.profile_picture)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# ==============================
# PUBLICATIONS
# ==============================
class Publications(models.Model, ImageOptimizeMixin):
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    download = models.FileField(upload_to="publications/", blank=True, null=True)
    publication_image = models.ImageField(
        upload_to="publications/images/", blank=True, null=True
    )

    def save(self, *args, **kwargs):
        if self.publication_image:
            self.optimize_image(self.publication_image)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# ==============================
# BOARD MEMBERS
# ==============================
class BoardMember(models.Model, ImageOptimizeMixin):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to="board_members/", default="default.jpg")
    position = models.CharField(max_length=255, default="Board Member")
    about = models.TextField()
    linkedin = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)

    # Changed: no auto_now_add, editable date field
    joined_at = models.DateTimeField(
        verbose_name="Joined Date",
        help_text="Date this board member joined (used for ordering)",
        blank=True,  # allow empty if you don't know yet
        null=True,
        db_index=True,  # faster sorting
    )

    class Meta:
        ordering = ["-joined_at", "name"]  # newest joined first, then name
        verbose_name = "Board Member"
        verbose_name_plural = "Board Members"

    def save(self, *args, **kwargs):
        if self.image:
            self.optimize_image(self.image)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("board_member_detail", args=[self.pk])


class Category(models.Model):
    """News categories (e.g. Projects, Company Updates, Industry News, Sustainability)"""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class NewsArticle(models.Model):
    """Main news / article model"""

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300, unique=True, blank=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles",
    )

    featured_image = models.ImageField(
        upload_to="news/images/%Y/%m/%d/", blank=True, null=True
    )

    excerpt = models.TextField(
        max_length=300, help_text="Short summary (displayed in lists/cards)"
    )

    content = models.TextField()  # main article body

    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="news_articles",
    )

    # Publishing control
    is_published = models.BooleanField(default=False)
    publish_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # SEO & sharing
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.CharField(max_length=320, blank=True)

    # Optional fields
    tags = models.CharField(
        max_length=300, blank=True, help_text="Comma separated tags"
    )
    is_featured = models.BooleanField(
        default=False, help_text="Show in featured/highlight section"
    )
    views_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-publish_date"]
        indexes = [
            models.Index(fields=["-publish_date"]),
            models.Index(fields=["is_published", "publish_date"]),
            models.Index(fields=["slug"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        # Auto-fill meta if empty
        if not self.meta_title:
            self.meta_title = self.title
        if not self.meta_description:
            self.meta_description = self.excerpt[:320]

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def display_date(self):
        return self.publish_date.strftime("%d %b %Y")


class NewsImage(models.Model):
    """Multiple images inside one article (gallery)"""

    article = models.ForeignKey(
        NewsArticle, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="news/gallery/%Y/%m/%d/")
    caption = models.CharField(max_length=255, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Image for {self.article.title}"


class ExternalAuthor(models.Model):
    """If you want news written by external people (not site users)"""

    name = models.CharField(max_length=150)
    title = models.CharField(
        max_length=100, blank=True
    )  # e.g. Senior Architect, Partner
    photo = models.ImageField(upload_to="news/authors/", blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Branch(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    latitude = models.FloatField(
        null=True,  # ← allow database NULL
        blank=True,  # ← allow blank in forms/admin
        help_text="e.g., 5.6037 for Accra",
    )
    longitude = models.FloatField(
        null=True, blank=True, help_text="e.g., -0.1870 for Accra"
    )
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Branches"
