from django.db import models
from django.utils.text import slugify


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


class Project(models.Model):
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

    total_floor_area = models.CharField(max_length=100, help_text="e.g. 5,000 sqm")

    start_date = models.DateField()
    completed_date = models.DateField(blank=True, null=True)

    job_sheets = models.CharField(max_length=300, blank=True)
    certificate = models.CharField(max_length=300, blank=True)

    category = models.ForeignKey(
        ProjectCategory, on_delete=models.SET_NULL, null=True, related_name="projects"
    )

    created_at = models.DateTimeField(auto_now_add=True)

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


class ProjectImage(models.Model):
    PROJECT_PICTURE = "project"
    CONSTRUCTION_PICTURE = "construction"

    IMAGE_TYPE_CHOICES = [
        (PROJECT_PICTURE, "Project Pictures"),
        (CONSTRUCTION_PICTURE, "Construction Pictures"),
    ]

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="gallery"
    )

    image = models.ImageField(upload_to="projects/gallery/")
    image_type = models.CharField(max_length=20, choices=IMAGE_TYPE_CHOICES)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project.title} - {self.image_type}"
