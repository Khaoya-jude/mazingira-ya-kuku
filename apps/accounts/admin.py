from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import FarmerUser, FarmRecord

@admin.register(FarmerUser)
class FarmerUserAdmin(UserAdmin):
    list_display = ["username", "get_full_name", "phone", "county", "farm_scale", "total_birds"]
    list_filter = ["county", "farm_scale", "sms_alerts"]
    fieldsets = UserAdmin.fieldsets + (
        ("Farm Details", {"fields": ("phone", "county", "sub_location", "farm_scale", "total_birds", "sms_alerts")}),
    )

@admin.register(FarmRecord)
class FarmRecordAdmin(admin.ModelAdmin):
    list_display = ["farmer", "week_start", "eggs_produced", "revenue_kes", "feed_cost_kes"]
    list_filter = ["week_start"]
