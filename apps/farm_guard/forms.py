from django import forms
from .models import DiseaseAlert, VaccinationRecord

class DiseaseAlertForm(forms.ModelForm):
    class Meta:
        model = DiseaseAlert
        fields = ["disease", "disease_name_freetext", "birds_affected", "birds_dead",
                  "severity", "description", "image"]

class VaccinationRecordForm(forms.ModelForm):
    class Meta:
        model = VaccinationRecord
        fields = ["disease", "vaccine_name", "supplier", "batch_number",
                  "birds_vaccinated", "date_administered", "next_due_date", "notes"]
        widgets = {
            "date_administered": forms.DateInput(attrs={"type": "date"}),
            "next_due_date": forms.DateInput(attrs={"type": "date"}),
        }
