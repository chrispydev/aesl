from django.db import models
from django.urls import reverse
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

    def __str__(self):
        return f"{self.project.title} - {self.image_type}"


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


class Staff(models.Model):
    sub_category = models.ForeignKey(
        SubCategory, on_delete=models.CASCADE, related_name="staff"
    )
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to="staff_images/", blank=True, null=True)
    grade = models.CharField(max_length=100)
    region = models.CharField(
        max_length=100, null=False, blank=True, default="Not a Regional Head"
    )
    email = models.EmailField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)
    profession = models.CharField(max_length=255)
    department = models.CharField(max_length=255, default="tech")

    # Social media links
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Publications(models.Model):
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    download = models.FileField(upload_to="publications/", blank=True, null=True)


class BoardMember(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to="board_members/", default="default.jpg")
    position = models.CharField(max_length=255, default="Board Member")
    about = models.TextField()

    linkedin = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("board_member_detail", args=[self.pk])
