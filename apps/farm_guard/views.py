from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import DiseaseAlert, Disease, VaccinationRecord, SymptomCheckerSession
from .forms import DiseaseAlertForm, VaccinationRecordForm


def alert_map(request):
    """Public disease alert map for Nairobi region."""
    thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
    alerts = DiseaseAlert.objects.filter(
        created_at__gte=thirty_days_ago
    ).select_related("disease").order_by("-created_at")

    critical_alerts = alerts.filter(severity="confirmed")
    diseases = Disease.objects.all()

    return render(request, "farm_guard/alert_map.html", {
        "alerts": alerts[:50],
        "critical_alerts": critical_alerts[:5],
        "diseases": diseases,
        "alert_count": alerts.count(),
    })


@login_required
def report_alert(request):
    """Farmer reports a sick flock."""
    if request.method == "POST":
        form = DiseaseAlertForm(request.POST, request.FILES)
        if form.is_valid():
            alert = form.save(commit=False)
            alert.reported_by = request.user
            alert.county = request.user.county
            alert.sub_location = request.user.sub_location
            alert.save()
            # In production: trigger SMS broadcast to nearby farmers
            messages.warning(
                request,
                "Alert reported. Nearby farmers will be notified via SMS. "
                "Please contact a vet if you haven't already."
            )
            return redirect("farm_guard:alerts")
    else:
        form = DiseaseAlertForm()
    return render(request, "farm_guard/report_alert.html", {"form": form})


def symptom_checker(request):
    """Simple symptom → likely disease tool."""
    diseases = Disease.objects.all()
    result = None

    if request.method == "POST":
        selected_symptoms = request.POST.getlist("symptoms")
        # Simple keyword matching — production would use a weighted scoring
        best_match = None
        best_score = 0
        for disease in diseases:
            disease_symptoms = set(s.lower() for s in disease.symptoms_list())
            selected_set = set(s.lower() for s in selected_symptoms)
            score = len(disease_symptoms & selected_set)
            if score > best_score:
                best_score = score
                best_match = disease

        result = best_match if best_score > 0 else None

        # Log session
        if request.user.is_authenticated:
            SymptomCheckerSession.objects.create(
                farmer=request.user,
                symptoms_reported=", ".join(selected_symptoms),
                suggested_disease=result,
                vet_referral_triggered=(result and result.emergency_level in ["high", "critical"]),
            )

    symptom_options = [
        "Sudden death", "Reduced egg production", "Diarrhoea",
        "Sneezing / coughing", "Swollen face", "Loss of appetite",
        "Twisted neck", "Pale comb", "Ruffled feathers", "Mucus discharge",
        "Paralysis", "Blood in droppings", "Green diarrhoea",
    ]

    return render(request, "farm_guard/symptom_checker.html", {
        "diseases": diseases,
        "symptom_options": symptom_options,
        "result": result,
    })


@login_required
def vaccination_log(request):
    records = VaccinationRecord.objects.filter(farmer=request.user).order_by("-date_administered")
    upcoming = records.filter(next_due_date__gte=timezone.now().date()).order_by("next_due_date")

    if request.method == "POST":
        form = VaccinationRecordForm(request.POST)
        if form.is_valid():
            rec = form.save(commit=False)
            rec.farmer = request.user
            rec.save()
            messages.success(request, "Vaccination record saved.")
            return redirect("farm_guard:vaccination_log")
    else:
        form = VaccinationRecordForm()

    return render(request, "farm_guard/vaccination_log.html", {
        "records": records,
        "upcoming": upcoming,
        "form": form,
    })
