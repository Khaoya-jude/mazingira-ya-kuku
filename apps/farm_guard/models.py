from django.db import models
from django.utils.translation import gettext_lazy as _


class Disease(models.Model):
    """Disease knowledge base entry."""
    name = models.CharField(max_length=200)
    swahili_name = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    symptoms = models.TextField(help_text="Comma-separated list of symptoms")
    prevention = models.TextField()
    treatment = models.TextField()
    emergency_level = models.CharField(
        max_length=10,
        choices=[("low", "Low"), ("medium", "Medium"), ("high", "High"), ("critical", "Critical")],
        default="medium",
    )
    image = models.ImageField(upload_to="diseases/", blank=True)

    def __str__(self):
        return self.name

    def symptoms_list(self):
        return [s.strip() for s in self.symptoms.split(",")]


class DiseaseAlert(models.Model):
    """Geo-tagged disease outbreak report from a farmer."""

    SEVERITY = [
        ("suspected", "Suspected — not confirmed"),
        ("confirmed", "Confirmed by vet"),
        ("resolved", "Resolved"),
    ]

    reported_by = models.ForeignKey(
        "accounts.FarmerUser", on_delete=models.SET_NULL, null=True, related_name="alerts"
    )
    disease = models.ForeignKey(Disease, on_delete=models.SET_NULL, null=True, blank=True)
    disease_name_freetext = models.CharField(max_length=200, blank=True, help_text="If disease unknown")
    county = models.CharField(max_length=50, default="nairobi")
    sub_location = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    birds_affected = models.PositiveIntegerField(default=0)
    birds_dead = models.PositiveIntegerField(default=0)
    severity = models.CharField(max_length=20, choices=SEVERITY, default="suspected")
    description = models.TextField()
    image = models.ImageField(upload_to="alerts/", blank=True)
    verified_by_vet = models.BooleanField(default=False)
    sms_broadcast_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Alert: {self.disease or self.disease_name_freetext} in {self.sub_location}"


class VaccinationRecord(models.Model):
    """Track farmer's vaccination schedule."""
    farmer = models.ForeignKey(
        "accounts.FarmerUser", on_delete=models.CASCADE, related_name="vaccinations"
    )
    disease = models.ForeignKey(Disease, on_delete=models.PROTECT)
    vaccine_name = models.CharField(max_length=200)
    supplier = models.CharField(max_length=200)
    batch_number = models.CharField(max_length=100, blank=True)
    birds_vaccinated = models.PositiveIntegerField()
    date_administered = models.DateField()
    next_due_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_administered"]

    def __str__(self):
        return f"{self.farmer} — {self.vaccine_name} on {self.date_administered}"


class SymptomCheckerSession(models.Model):
    """Log of farmer using the symptom checker tool."""
    farmer = models.ForeignKey(
        "accounts.FarmerUser", on_delete=models.SET_NULL, null=True
    )
    symptoms_reported = models.TextField()
    suggested_disease = models.ForeignKey(Disease, on_delete=models.SET_NULL, null=True, blank=True)
    vet_referral_triggered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
