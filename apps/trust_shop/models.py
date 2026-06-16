from django.db import models


class VerifiedSupplier(models.Model):
    SUPPLIER_TYPES = [
        ("feed", "Feed Supplier"), ("agrovet", "Agro-Vet Shop"),
        ("chick", "Day-Old Chick Supplier"), ("equipment", "Equipment & Housing"),
        ("vet", "Veterinary Service"),
    ]
    name = models.CharField(max_length=200)
    supplier_type = models.CharField(max_length=20, choices=SUPPLIER_TYPES)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=300)
    county = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    verified = models.BooleanField(default=False)
    verified_date = models.DateField(null=True, blank=True)
    verification_body = models.CharField(max_length=200, blank=True)
    qr_token = models.CharField(max_length=64, unique=True, blank=True)
    logo = models.ImageField(upload_to="suppliers/", blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    review_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_supplier_type_display()})"

    @property
    def trust_badge(self):
        return "✓ Verified" if self.verified else "Unverified"


class SupplierReview(models.Model):
    supplier = models.ForeignKey(VerifiedSupplier, on_delete=models.CASCADE, related_name="reviews")
    reviewer = models.ForeignKey("accounts.FarmerUser", on_delete=models.SET_NULL, null=True)
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    review_text = models.TextField()
    purchased_item = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
