from django.db import models
from django.utils.translation import gettext_lazy as _


class EggListing(models.Model):
    """Farmer's egg supply listing."""

    GRADE_CHOICES = [
        ("A", "Grade A (Large)"),
        ("B", "Grade B (Medium)"),
        ("C", "Grade C (Small)"),
        ("mixed", "Mixed"),
    ]

    farmer = models.ForeignKey(
        "accounts.FarmerUser", on_delete=models.CASCADE, related_name="listings"
    )
    grade = models.CharField(max_length=10, choices=GRADE_CHOICES)
    quantity_trays = models.PositiveIntegerField(help_text="Number of 30-egg trays available")
    price_per_tray = models.DecimalField(max_digits=8, decimal_places=2, help_text="KES per tray")
    available_from = models.DateField()
    available_until = models.DateField()
    delivery_available = models.BooleanField(default=False)
    pickup_location = models.CharField(max_length=300)
    county = models.CharField(max_length=50, default="nairobi")
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.farmer} — {self.quantity_trays} trays Grade {self.grade} @ KES {self.price_per_tray}"


class BuyerInquiry(models.Model):
    """A buyer (hotel, retailer, individual) expressing interest in a listing."""

    BUYER_TYPES = [
        ("individual", "Individual / Household"),
        ("retailer", "Retailer / Shop"),
        ("restaurant", "Restaurant / Hotel"),
        ("institution", "School / Hospital / Institution"),
        ("wholesaler", "Wholesaler"),
    ]

    STATUS = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("declined", "Declined"),
        ("completed", "Completed"),
    ]

    listing = models.ForeignKey(EggListing, on_delete=models.CASCADE, related_name="inquiries")
    buyer_name = models.CharField(max_length=200)
    buyer_type = models.CharField(max_length=20, choices=BUYER_TYPES)
    buyer_phone = models.CharField(max_length=20)
    buyer_email = models.EmailField(blank=True)
    trays_requested = models.PositiveIntegerField()
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry: {self.buyer_name} → {self.listing}"


class MarketPrice(models.Model):
    """Nairobi market egg price index (admin-curated + crowdsourced)."""
    location = models.CharField(max_length=100)
    grade = models.CharField(max_length=10, choices=EggListing.GRADE_CHOICES)
    price_per_tray = models.DecimalField(max_digits=8, decimal_places=2)
    date_observed = models.DateField()
    source = models.CharField(max_length=100, default="crowdsourced")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_observed"]
