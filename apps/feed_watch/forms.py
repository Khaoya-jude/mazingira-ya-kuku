from django import forms
from .models import FeedPrice, BulkBuyGroup

class FeedPriceForm(forms.ModelForm):
    class Meta:
        model = FeedPrice
        fields = ["feed_type", "brand", "price_per_50kg", "location", "county", "date_observed"]
        widgets = {"date_observed": forms.DateInput(attrs={"type": "date"})}

class BulkBuyGroupForm(forms.ModelForm):
    class Meta:
        model = BulkBuyGroup
        fields = ["feed_type", "target_bags", "target_date", "pickup_location",
                  "max_members", "estimated_saving_pct", "description"]
        widgets = {"target_date": forms.DateInput(attrs={"type": "date"})}
