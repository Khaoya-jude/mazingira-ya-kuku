from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import EggListing, BuyerInquiry, MarketPrice

def listing_list(request):
    county = request.GET.get("county", "nairobi")
    grade = request.GET.get("grade", "")
    listings = EggListing.objects.filter(is_active=True)
    if county:
        listings = listings.filter(county=county)
    if grade:
        listings = listings.filter(grade=grade)
    return render(request, "egg_market/listings.html", {
        "listings": listings, "county": county, "grade": grade,
        "grade_choices": EggListing.GRADE_CHOICES,
    })

@login_required
def create_listing(request):
    if request.method == "POST":
        EggListing.objects.create(
            farmer=request.user,
            grade=request.POST.get("grade"),
            quantity_trays=int(request.POST.get("quantity_trays", 0)),
            price_per_tray=request.POST.get("price_per_tray"),
            available_from=request.POST.get("available_from"),
            available_until=request.POST.get("available_until"),
            pickup_location=request.POST.get("pickup_location"),
            county=request.user.county,
            delivery_available=request.POST.get("delivery_available") == "on",
        )
        messages.success(request, "Egg listing created! Buyers can now find you.")
        return redirect("egg_market:listings")
    return render(request, "egg_market/create_listing.html", {"grade_choices": EggListing.GRADE_CHOICES})

def listing_detail(request, pk):
    listing = get_object_or_404(EggListing, pk=pk)
    if request.method == "POST":
        BuyerInquiry.objects.create(
            listing=listing,
            buyer_name=request.POST.get("buyer_name"),
            buyer_type=request.POST.get("buyer_type"),
            buyer_phone=request.POST.get("buyer_phone"),
            trays_requested=int(request.POST.get("trays_requested", 1)),
            message=request.POST.get("message", ""),
        )
        messages.success(request, "Inquiry sent to farmer!")
    return render(request, "egg_market/listing_detail.html", {
        "listing": listing,
        "buyer_types": BuyerInquiry.BUYER_TYPES,
    })

def market_prices(request):
    prices = MarketPrice.objects.order_by("-date_observed")[:50]
    return render(request, "egg_market/market_prices.html", {"prices": prices})
