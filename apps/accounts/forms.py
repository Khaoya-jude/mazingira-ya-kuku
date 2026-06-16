from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import FarmerUser, FarmRecord

class FarmerRegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone = forms.CharField(required=False, help_text="e.g. 0712345678")

    class Meta:
        model = FarmerUser
        fields = ["username", "first_name", "last_name", "phone", "password1", "password2"]

class FarmerProfileForm(forms.ModelForm):
    class Meta:
        model = FarmerUser
        fields = ["first_name", "last_name", "phone", "county", "sub_location",
                  "farm_scale", "total_birds", "sms_alerts", "avatar"]

class FarmRecordForm(forms.ModelForm):
    class Meta:
        model = FarmRecord
        fields = ["week_start", "eggs_produced", "eggs_sold", "revenue_kes",
                  "feed_cost_kes", "mortality", "notes"]
        widgets = {"week_start": forms.DateInput(attrs={"type": "date"})}
