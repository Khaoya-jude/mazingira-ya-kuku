def farmer_context(request):
    """Inject farmer-specific context into all templates."""
    ctx = {}
    if request.user.is_authenticated:
        ctx["farmer_bird_count"] = request.user.total_birds
        ctx["profile_complete"] = request.user.profile_complete
    return ctx
