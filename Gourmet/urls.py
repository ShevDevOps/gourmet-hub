"""
URL configuration for Gourmet project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from order_table import views as order_views
from dishes import views as dishes_views
from shefs import views as shefs_views
from Gourmet import views
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dishes_views.index, name='index'),
    path('order/', order_views.order_table, name='order_table'),
    path('shefs/', shefs_views.shefs, name='shefs'),
    path('dishes/', include('dishes.urls')),
    path('shefs/<int:shef_id>/', shefs_views.shef_detail, name='shef_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)