from django.shortcuts import render
from .models import *
from django.db.models import Q, Prefetch

def index(request):
    return render(request, 'index.html')

def dishes(request):
    # Start with all dishes, optimizing related object fetching
    dishes_queryset = Dish.objects.select_related('standard_category').prefetch_related('recommendation_tags').all()

    # Get filter options
    standard_categories = StandardCategory.objects.all()
    recommendation_tags = RecommendationTag.objects.all()

    # Get filter parameters from GET request
    search_query = request.GET.get('search', '').strip()
    selected_std_category_id = request.GET.get('standard_category', '')
    selected_rec_tag_id = request.GET.get('recommendation_tag', '')
    filter_vegetarian = request.GET.get('vegetarian', '') == 'on'
    filter_spicy = request.GET.get('spicy', '') == 'on'

    # Apply search filter
    if search_query:
        dishes_queryset = dishes_queryset.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(ingredients_list__name__icontains=search_query) |
            Q(standard_category__name__icontains=search_query) |
            Q(recommendation_tags__name__icontains=search_query)
        ).distinct()

    # Apply standard category filter
    if selected_std_category_id and selected_std_category_id.isdigit():
        dishes_queryset = dishes_queryset.filter(standard_category_id=int(selected_std_category_id))

    # Apply recommendation tag filter
    if selected_rec_tag_id and selected_rec_tag_id.isdigit():
        dishes_queryset = dishes_queryset.filter(recommendation_tags__id=int(selected_rec_tag_id))

    # Apply boolean filters
    if filter_vegetarian:
        dishes_queryset = dishes_queryset.filter(is_vegetarian=True)
    if filter_spicy:
        dishes_queryset = dishes_queryset.filter(is_spicy=True)

    context = {
        'dishes': dishes_queryset,
        'standard_categories': standard_categories,
        'recommendation_tags': recommendation_tags,
        'search_query': search_query,
        'selected_standard_category_id': selected_std_category_id,
        'selected_tag_id': selected_rec_tag_id,
        'filter_vegetarian': filter_vegetarian,
        'filter_spicy': filter_spicy,
    }
    return render(request, 'dishes.html', context)