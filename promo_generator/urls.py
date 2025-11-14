from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('promo/<int:promo_id>/', views.promo_detail, name='promo_detail'),
    path('list/', views.promo_list, name='promo_list'),
    path('api/test/', views.api_test, name='api_test'),
]
