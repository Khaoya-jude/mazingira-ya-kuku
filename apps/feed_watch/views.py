from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Min, Max, Count
from django.utils import timezone
from .models import FeedPrice, BulkBuyGroup, BulkBuyMembership, FeedSupplier
from .forms import FeedPriceForm, BulkBuyGroupForm


def price_list(request):
    """Main feed price board — public."""
    county = request.GET.get("county", "nairobi")
    feed_type = request.GET.get("feed_type", "layers_mash")
    thirty_days_ago = timezone.now().date() - timezone.timedelta(days=30)

    prices = FeedPrice.objects.filter(
        county=county, date_observed__gte=thirty_days_ago
    ).order_by("price_per_50kg")

    if feed_type:
        prices = prices.filter(feed_type=feed_type)

    stats = prices.aggregate(
        avg=Avg("price_per_50kg"),
        low=Min("price_per_50kg"),
        high=Max("price_per_50kg"),
    )

    bulk_groups = BulkBuyGroup.objects.filter(county=county, status="open")[:5]

    return render(request, "feed_watch/price_list.html", {
        "prices": prices[:30],
        "stats": stats,
        "bulk_groups": bulk_groups,
        "county": county,
        "feed_type": feed_type,
        "feed_type_choices": FeedPrice.FEED_TYPES,
    })


@login_required
def submit_price(request):
    """Crowdsource a new price observation."""
    if request.method == "POST":
        form = FeedPriceForm(request.POST)
        if form.is_valid():
            price = form.save(commit=False)
            price.submitted_by = request.user
            price.save()
            messages.success(request, "Price submitted — asante! It helps all farmers.")
            return redirect("feed_watch:prices")
    else:
        form = FeedPriceForm(initial={"county": request.user.county})
    return render(request, "feed_watch/submit_price.html", {"form": form})


@login_required
def bulk_buy_list(request):
    county = request.GET.get("county", request.user.county)
    groups = BulkBuyGroup.objects.filter(status="open").order_by("target_date")
    return render(request, "feed_watch/bulk_buy_list.html", {"groups": groups, "county": county})


@login_required
def join_bulk_group(request, group_id):
    group = get_object_or_404(BulkBuyGroup, pk=group_id, status="open")
    if group.spots_left == 0:
        messages.error(request, "This group is full.")
        return redirect("feed_watch:bulk_buy")

    membership, created = BulkBuyMembership.objects.get_or_create(
        group=group, farmer=request.user,
        defaults={"bags_needed": int(request.POST.get("bags_needed", 1))}
    )
    if created:
        messages.success(request, f"You've joined the bulk-buy group! Contact {group.organiser} to coordinate.")
    else:
        messages.info(request, "You're already in this group.")
    return redirect("feed_watch:bulk_buy")


@login_required
def create_bulk_group(request):
    if request.method == "POST":
        form = BulkBuyGroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.organiser = request.user
            group.county = request.user.county
            group.save()
            messages.success(request, "Bulk-buy group created! Share it with your network.")
            return redirect("feed_watch:bulk_buy")
    else:
        form = BulkBuyGroupForm()
    return render(request, "feed_watch/create_bulk_group.html", {"form": form})
