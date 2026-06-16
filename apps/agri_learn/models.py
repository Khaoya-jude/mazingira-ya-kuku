from django.db import models


class Article(models.Model):
    CATEGORIES = [
        ("feed", "Feed Management"), ("health", "Flock Health"),
        ("housing", "Housing & Biosecurity"), ("market", "Market Access"),
        ("finance", "Farm Finance"), ("regulation", "Regulation & Standards"),
    ]
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    summary = models.CharField(max_length=500)
    content = models.TextField()
    sms_version = models.CharField(max_length=160, blank=True)
    author = models.CharField(max_length=200, default="Platform Team")
    is_published = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to="articles/", blank=True)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class VetDirectory(models.Model):
    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=200, default="Veterinary Officer")
    county = models.CharField(max_length=50)
    sub_location = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    specialisation = models.CharField(max_length=200, blank=True)
    available_for_farm_visits = models.BooleanField(default=True)
    dvs_registered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Vet directory"

    def __str__(self):
        return f"Dr. {self.name} — {self.county}"


class AskExpert(models.Model):
    STATUS = [("open", "Open"), ("answered", "Answered"), ("closed", "Closed")]
    farmer = models.ForeignKey("accounts.FarmerUser", on_delete=models.SET_NULL, null=True)
    question = models.TextField()
    answer = models.TextField(blank=True)
    answered_by = models.ForeignKey(VetDirectory, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default="open")
    created_at = models.DateTimeField(auto_now_add=True)
    answered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.question[:80]
