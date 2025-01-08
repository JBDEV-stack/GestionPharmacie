from django.urls import path
from . import views

urlpatterns = [
    path('stocks_dashboard/', views.stocks_dashboard, name='stocks_dashboard'),
    path('categories/', views.categories_index, name='categories_index'),
    path('categories/create/', views.categories_create, name='categories_create'),
    path('categories/edit/<int:id>/', views.categories_edit, name='categories_edit'),
    path('categories/delete/<int:id>/', views.categories_delete, name='categories_delete'),
    path('medicaments/', views.medicaments_index, name='medicaments_index'),
    path('medicaments/create/', views.medicament_create, name='medicament_create'),
    path('medicaments/update/<int:id_Medicament>/', views.medicament_update, name='medicament_update'),
    path('medicaments/hide/<int:id>/', views.medicament_hide, name='medicament_hide'),
    path('stocks/', views.stocks_index, name='stocks_index'),
    path('stocks/create/', views.stocks_create, name='stocks_create'),
    path('stocks/update/<int:id>/', views.stocks_update, name='stocks_update'),
    path('stocks/delete/<int:id>/', views.stocks_delete, name='stocks_delete'),
    path('stocks/get/<int:id>/', views.get_stock_for_update, name='get_stock_for_update'),
    path('fournisseurs/', views.fournisseurs_index, name='fournisseurs_index'),
    path('fournisseurs/create/', views.fournisseur_create, name='fournisseur_create'),
    path('fournisseurs/update/<int:pk>/', views.fournisseur_update, name='modifier_fournisseur'),
    path('fournisseurs/delete/<int:pk>/', views.fournisseur_delete, name='supprimer_fournisseur'),
    path('fournisseurs/search/', views.fournisseurs_search, name='fournisseurs_search'),
    path('commandes/', views.commandes_index, name='commandes_index'),
    path('commandes/create/', views.commandes_create, name='commandes_create'),
    path('commandes/update/<int:pk>/', views.commandes_update, name='commandes_update'),
    path('commandes/delete/<int:pk>/', views.commandes_delete, name='commandes_delete'),
    path('commandes/change_status/<int:pk>/', views.commandes_change_status, name='commandes_change_status'),
    path('notifications/', views.notifications_index, name='notifications_index'),
]
