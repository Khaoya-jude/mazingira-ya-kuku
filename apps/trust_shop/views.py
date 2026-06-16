from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import VerifiedSupplier, SupplierReview

def supplier_directory(request):
    supplier_type = request.GET.get("type", "")
    suppliers = VerifiedSupplier.objects.all().order_by("-verified", "-rating")
    if supplier_type:
        suppliers = suppliers.filter(supplier_type=supplier_type)
    return render(request, "trust_shop/directory.html", {
        "suppliers": suppliers,
        "supplier_types": VerifiedSupplier.SUPPLIER_TYPES,
        "selected_type": supplier_type,
    })

def verify_supplier(request, qr_token):
    supplier = get_object_or_404(VerifiedSupplier, qr_token=qr_token)
    return render(request, "trust_shop/verify.html", {"supplier": supplier})

def supplier_detail(request, pk):
    supplier = get_object_or_404(VerifiedSupplier, pk=pk)
    return render(request, "trust_shop/detail.html", {"supplier": supplier})

@login_required
def add_review(request, pk):
    from django.contrib import messages
    from django.shortcuts import redirect
    supplier = get_object_or_404(VerifiedSupplier, pk=pk)
    if request.method == "POST":
        SupplierReview.objects.create(
            supplier=supplier, reviewer=request.user,
            rating=int(request.POST.get("rating", 3)),
            review_text=request.POST.get("review_text", ""),
            purchased_item=request.POST.get("purchased_item", ""),
        )
        messages.success(request, "Review submitted — asante!")
    return redirect("trust_shop:detail", pk=pk)
