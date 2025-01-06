from django.urls import path
from . import views

urlpatterns = [
    path('pos/', views.pos_index, name='pos_index'),
    path('sales_dashboard/', views.sales_dashboard, name='sales_dashboard'),
    path('ventes/', views.ventes_index, name='ventes_index'),
    path('ventes/detail/<int:id>/', views.vente_detail, name='vente_detail'),
    path('filter_by_category/', views.filter_by_category, name='filter_by_category'),
    path('search_medicaments/', views.search_medicaments, name='search_medicaments'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('finalize_sale/', views.finalize_sale, name='finalize_sale'),
    path('search_ventes/', views.search_ventes, name='search_ventes'),  
]
