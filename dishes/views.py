from django.shortcuts import render, get_object_or_404
from .models import *
from django.db.models import Q, Prefetch, Min, Max

def index(request):
    return render(request, 'index.html')

def dish_detail(request, dish_id):
    dish = get_object_or_404(
        Dish.objects.select_related('standard_category')
                     .prefetch_related(
                         'recommendation_tags',
                         Prefetch('ingrtodish_set', queryset=IngrToDish.objects.select_related('ingredient'))
                     ),
        pk=dish_id
    )
    context = {
        'dish': dish
    }
    return render(request, 'dish_detail.html', context)

def dishes(request):
    dishes_queryset = Dish.objects.select_related('standard_category').prefetch_related('recommendation_tags').all()

    standard_categories_all = StandardCategory.objects.all().order_by('name')
    recommendation_tags_all = RecommendationTag.objects.all().order_by('name')

    search_query = request.GET.get('search', '').strip()
    selected_std_category_ids = request.GET.getlist('standard_category')
    selected_rec_tag_ids = request.GET.getlist('recommendation_tag')

    filter_vegetarian = request.GET.get('vegetarian', '') == 'on'
    filter_spicy = request.GET.get('spicy', '') == 'on'

    min_price_str = request.GET.get('min_price', '').strip()
    max_price_str = request.GET.get('max_price', '').strip()

    price_range_data = Dish.objects.all().aggregate(
        actual_min_price=Min('price'),
        actual_max_price=Max('price')
    )
    overall_min_price = price_range_data['actual_min_price'] if price_range_data['actual_min_price'] is not None else 0.0
    overall_max_price = price_range_data['actual_max_price'] if price_range_data['actual_max_price'] is not None else 1000.0

    if overall_min_price == overall_max_price:
        if Dish.objects.exists():
             overall_max_price = overall_min_price + 100
        else:
             overall_max_price = 1000.0
             overall_min_price = 0.0

    current_min_price = None
    if min_price_str:
        try:
            current_min_price = float(min_price_str)
        except ValueError:
            pass

    current_max_price = None
    if max_price_str:
        try:
            current_max_price = float(max_price_str)
        except ValueError:
            pass

    if search_query:
        dishes_queryset = dishes_queryset.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(ingredients_list__name__icontains=search_query) |
            Q(standard_category__name__icontains=search_query) |
            Q(recommendation_tags__name__icontains=search_query)
        ).distinct()

    if selected_std_category_ids:
        valid_category_ids = [int(id_str) for id_str in selected_std_category_ids if id_str.isdigit()]
        if valid_category_ids:
            dishes_queryset = dishes_queryset.filter(standard_category_id__in=valid_category_ids)

    if selected_rec_tag_ids:
        valid_tag_ids = [int(id_str) for id_str in selected_rec_tag_ids if id_str.isdigit()]
        if valid_tag_ids:
            dishes_queryset = dishes_queryset.filter(recommendation_tags__id__in=valid_tag_ids).distinct()

    if filter_vegetarian:
        dishes_queryset = dishes_queryset.filter(is_vegetarian=True)
    if filter_spicy:
        dishes_queryset = dishes_queryset.filter(is_spicy=True)

    if current_min_price is not None:
        dishes_queryset = dishes_queryset.filter(price__gte=current_min_price)

    if current_max_price is not None:
        dishes_queryset = dishes_queryset.filter(price__lte=current_max_price)

    dishes_queryset = dishes_queryset.order_by('standard_category__name', 'name')

    initial_min_slider = current_min_price if current_min_price is not None else overall_min_price
    initial_max_slider = current_max_price if current_max_price is not None else overall_max_price

    initial_min_slider = max(overall_min_price, min(initial_min_slider, overall_max_price))
    initial_max_slider = min(overall_max_price, max(initial_max_slider, overall_min_price))
    if initial_min_slider > initial_max_slider:
        initial_max_slider = initial_min_slider

    price_slider_js_config = {
        'overallMin': overall_min_price,
        'overallMax': overall_max_price,
        'initialMin': initial_min_slider,
        'initialMax': initial_max_slider,
    }

    context = {
        'dishes': dishes_queryset,
        'standard_categories': standard_categories_all,
        'recommendation_tags': recommendation_tags_all,
        'search_query': search_query,
        'selected_standard_category_ids': selected_std_category_ids,
        'selected_tag_ids': selected_rec_tag_ids,
        'filter_vegetarian': filter_vegetarian,
        'filter_spicy': filter_spicy,

        'current_min_price_val': initial_min_slider,
        'current_max_price_val': initial_max_slider,
        'overall_min_price_slider': overall_min_price,
        'overall_max_price_slider': overall_max_price,

        'min_price_form': min_price_str,
        'max_price_form': max_price_str,

        'price_slider_js_config': price_slider_js_config,
    }
    return render(request, 'dishes.html', context)