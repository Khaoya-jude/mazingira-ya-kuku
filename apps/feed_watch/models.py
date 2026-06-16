from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords


class FeedSupplier(models.Model):
    """Verified feed supplier."""
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    county = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    verified = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    review_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class FeedPrice(models.Model):
    """Crowdsourced feed price submission."""

    FEED_TYPES = [
        ("chick_mash", "Chick Mash"),
        ("growers_mash", "Growers Mash"),
        ("layers_mash", "Layers Mash"),
        ("layers_pellets", "Layers Pellets"),
        ("concentrates", "Concentrates"),
    ]

    supplier = models.ForeignKey(FeedSupplier, on_delete=models.SET_NULL, null=True, blank=True)
    submitted_by = models.ForeignKey(
        "accounts.FarmerUser", on_delete=models.SET_NULL, null=True, related_name="feed_prices"
    )
    feed_type = models.CharField(max_length=30, choices=FEED_TYPES)
    brand = models.CharField(max_length=100, blank=True)
    price_per_50kg = models.DecimalField(max_digits=8, decimal_places=2, help_text="KES per 50kg bag")
    location = models.CharField(max_length=200)
    county = models.CharField(max_length=50, default="nairobi")
    date_observed = models.DateField()
    verified = models.BooleanField(default=False)
    upvotes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["-date_observed", "-created_at"]

    def __str__(self):
        return f"{self.get_feed_type_display()} @ {self.location} — KES {self.price_per_50kg}"


class BulkBuyGroup(models.Model):
    """Farmer cooperative bulk-purchase group."""

    STATUS_CHOICES = [
        ("open", "Open — accepting members"),
        ("confirmed", "Confirmed — purchasing soon"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    organiser = models.ForeignKey(
        "accounts.FarmerUser", on_delete=models.CASCADE, related_name="organised_groups"
    )
    feed_type = models.CharField(max_length=30, choices=FeedPrice.FEED_TYPES)
    target_bags = models.PositiveIntegerField(help_text="Total 50kg bags needed")
    target_date = models.DateField()
    pickup_location = models.CharField(max_length=300)
    county = models.CharField(max_length=50, default="nairobi")
    max_members = models.PositiveSmallIntegerField(default=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
    estimated_saving_pct = models.DecimalField(max_digits=4, decimal_places=1, default=10)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bulk buy: {self.get_feed_type_display()} — {self.county} ({self.status})"

    @property
    def member_count(self):
        return self.memberships.filter(active=True).count()

    @property
    def spots_left(self):
        return max(0, self.max_members - self.member_count)


class BulkBuyMembership(models.Model):
    group = models.ForeignKey(BulkBuyGroup, on_delete=models.CASCADE, related_name="memberships")
    farmer = models.ForeignKey("accounts.FarmerUser", on_delete=models.CASCADE)
    bags_needed = models.PositiveSmallIntegerField(default=1)
    active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("group", "farmer")]
