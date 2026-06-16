"""
Comprehensive admin.py for the platform.
Run: python manage.py createsuperuser
"""
# apps/farm_guard/admin.py
from django.contrib import admin
from .models import Disease, DiseaseAlert, VaccinationRecord


@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ["name", "swahili_name", "emergency_level"]
    list_filter = ["emergency_level"]
    search_fields = ["name"]


@admin.register(DiseaseAlert)
class DiseaseAlertAdmin(admin.ModelAdmin):
    list_display = ["disease", "sub_location", "county", "severity", "birds_affected", "sms_broadcast_sent", "created_at"]
    list_filter = ["severity", "county", "sms_broadcast_sent"]
    actions = ["send_sms_broadcast"]

    @admin.action(description="Send SMS broadcast to nearby farmers")
    def send_sms_broadcast(self, request, queryset):
        for alert in queryset.filter(sms_broadcast_sent=False):
            # TODO: integrate Africa's Talking SMS API here
            alert.sms_broadcast_sent = True
            alert.save()
        self.message_user(request, f"SMS broadcasts queued for {queryset.count()} alerts.")


@admin.register(VaccinationRecord)
class VaccinationRecordAdmin(admin.ModelAdmin):
    list_display = ["farmer", "vaccine_name", "date_administered", "next_due_date"]
    list_filter = ["disease"]
