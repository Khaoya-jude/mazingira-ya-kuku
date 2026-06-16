from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Article, VetDirectory, AskExpert

def article_list(request):
    category = request.GET.get("category", "")
    articles = Article.objects.filter(is_published=True)
    if category:
        articles = articles.filter(category=category)
    featured = articles.filter(featured=True)[:3]
    return render(request, "agri_learn/article_list.html", {
        "articles": articles, "featured": featured,
        "categories": Article.CATEGORIES, "selected_category": category,
    })

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, is_published=True)
    Article.objects.filter(pk=article.pk).update(views=article.views + 1)
    return render(request, "agri_learn/article_detail.html", {"article": article})

def vet_directory(request):
    county = request.GET.get("county", "nairobi")
    vets = VetDirectory.objects.filter(county=county)
    return render(request, "agri_learn/vet_directory.html", {"vets": vets, "county": county})

@login_required
def ask_expert(request):
    from django.contrib import messages
    from django.shortcuts import redirect
    if request.method == "POST":
        AskExpert.objects.create(farmer=request.user, question=request.POST.get("question", ""))
        messages.success(request, "Question submitted! A vet will respond within 48 hours.")
        return redirect("agri_learn:ask_expert")
    questions = AskExpert.objects.filter(status="answered").order_by("-answered_at")[:10]
    return render(request, "agri_learn/ask_expert.html", {"questions": questions})
