from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.db.models import Sum, Avg
from django.utils import timezone
from .models import FarmerUser, FarmRecord
from .forms import FarmerRegistrationForm, FarmerProfileForm, FarmRecordForm


@login_required
def dashboard(request):
    """Main farmer dashboard — production overview."""
    user = request.user
    ninety_days_ago = timezone.now().date() - timezone.timedelta(days=90)
    recent_records = FarmRecord.objects.filter(
        farmer=user, week_start__gte=ninety_days_ago
    ).order_by("week_start")

    totals = recent_records.aggregate(
        total_eggs=Sum("eggs_produced"),
        total_revenue=Sum("revenue_kes"),
        total_feed_cost=Sum("feed_cost_kes"),
        avg_mortality=Avg("mortality"),
    )

    # Weekly chart data for JS
    chart_labels = [r.week_start.strftime("%d %b") for r in recent_records]
    chart_eggs = [r.eggs_produced for r in recent_records]
    chart_profit = [float(r.profit_kes) for r in recent_records]

    return render(request, "accounts/dashboard.html", {
        "totals": totals,
        "recent_records": recent_records.order_by("-week_start")[:10],
        "chart_labels": chart_labels,
        "chart_eggs": chart_eggs,
        "chart_profit": chart_profit,
    })


@login_required
def log_record(request):
    """Log weekly farm production record. Updates if week already exists."""
    if request.method == "POST":
        form = FarmRecordForm(request.POST)
        if form.is_valid():
            week_start = form.cleaned_data["week_start"]
            # Get existing record for this week, or create new
            existing = FarmRecord.objects.filter(
                farmer=request.user, week_start=week_start
            ).first()
            if existing:
                form = FarmRecordForm(request.POST, instance=existing)
                form.save()
                messages.success(request, "Record updated for this week!")
            else:
                record = form.save(commit=False)
                record.farmer = request.user
                record.save()
                messages.success(request, "Record saved!")
            return redirect("dashboard_root:home")
    else:
        form = FarmRecordForm(initial={"week_start": timezone.now().date()})
    return render(request, "accounts/log_record.html", {"form": form})


@login_required
def profile(request):
    if request.method == "POST":
        form = FarmerProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated!")
            return redirect("dashboard_root:profile")
    else:
        form = FarmerProfileForm(instance=request.user)
    return render(request, "accounts/profile.html", {"form": form})


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard_root:home")
    if request.method == "POST":
        form = FarmerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.first_name}! Complete your farm profile to get started.")
            return redirect("dashboard_root:profile")
    else:
        form = FarmerRegistrationForm()
    return render(request, "accounts/register.html", {"form": form})


def farmer_login(request):
    if request.user.is_authenticated:
        return redirect("dashboard_root:home")
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password"),
        )
        if user:
            login(request, user)
            return redirect(request.GET.get("next", "dashboard_root:home"))
        messages.error(request, "Wrong username or password.")
    return render(request, "accounts/login.html")


def farmer_logout(request):
    logout(request)
    return redirect("landing")
