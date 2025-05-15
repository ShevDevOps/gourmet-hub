from django.urls import path
from . import views

app_name = 'dishes'

urlpatterns = [ 
    path('', views.dishes, name='dishes'),
    path('<int:dish_id>/', views.dish_detail, name='dish_detail'),
]