from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class FarmerUser(AbstractUser):
    """Extended user model for poultry farmers."""

    COUNTY_CHOICES = [
        ("nairobi", "Nairobi"),
        ("kiambu", "Kiambu"),
        ("kajiado", "Kajiado"),
        ("machakos", "Machakos"),
        ("muranga", "Murang'a"),
    ]

    SCALE_CHOICES = [
        ("small", "Small (< 500 birds)"),
        ("medium", "Medium (500–2,000 birds)"),
        ("large", "Large (> 2,000 birds)"),
    ]

    phone = PhoneNumberField(blank=True)
    county = models.CharField(max_length=50, choices=COUNTY_CHOICES, default="nairobi")
    sub_location = models.CharField(max_length=100, blank=True)
    farm_scale = models.CharField(max_length=20, choices=SCALE_CHOICES, default="small")
    total_birds = models.PositiveIntegerField(default=0)
    profile_complete = models.BooleanField(default=False)
    sms_alerts = models.BooleanField(default=True, help_text="Receive SMS disease alerts")
    joined_cooperative = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to="avatars/", blank=True)

    class Meta:
        verbose_name = _("Farmer")
        verbose_name_plural = _("Farmers")

    def __str__(self):
        return f"{self.get_full_name() or self.username} — {self.sub_location}"

    @property
    def initials(self):
        parts = self.get_full_name().split()
        return "".join(p[0].upper() for p in parts[:2]) if parts else self.username[:2].upper()


class FarmRecord(models.Model):
    """Weekly production snapshot per farmer."""
    farmer = models.ForeignKey(FarmerUser, on_delete=models.CASCADE, related_name="records")
    week_start = models.DateField()
    eggs_produced = models.PositiveIntegerField(default=0)
    eggs_sold = models.PositiveIntegerField(default=0)
    revenue_kes = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    feed_cost_kes = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    mortality = models.PositiveSmallIntegerField(default=0, help_text="Birds lost this week")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-week_start"]
        unique_together = [("farmer", "week_start")]

    def __str__(self):
        return f"{self.farmer} — {self.week_start}"

    @property
    def profit_kes(self):
        return self.revenue_kes - self.feed_cost_kes

    @property
    def feed_cost_per_egg(self):
        if self.eggs_produced:
            return self.feed_cost_kes / self.eggs_produced
        return 0
