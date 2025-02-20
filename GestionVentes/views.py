from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string  # Importer render_to_string
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Vente, DetailVente
from GestionStocks.models import Medicament, CategorieMedicament, Stock, Notification  # Importez depuis GestionStocks
from .forms import VenteForm, DetailVenteForm
from Utilisateurs.decorators import role_required
from django.db.models import Sum, DecimalField, IntegerField
from django.db.models.functions import Coalesce
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
import json
import logging
from django.db import transaction
from decimal import Decimal
from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)

@login_required
@role_required('gestionnaire_ventes')
def pos_index(request):
    username = request.user.username
    categories = CategorieMedicament.afficheLesCategories()
    medicaments = Medicament.Medicament_disponible()
    return render(request, 'pos/index.html', {'categories': categories, 'medicaments': medicaments, 'username': username})

@login_required
@role_required('gestionnaire_ventes')
def sales_dashboard(request):
    username = request.user.username
    today = timezone.now().date()
    ventes = Vente.objects.filter(dateVente__date=today)
    total_revenue = ventes.aggregate(
        total=Coalesce(Sum('totalVente', output_field=DecimalField()), Decimal('0.00'))
    )['total']

    top_medicament = (
        DetailVente.objects.values('id_Medicaments__nom')
        .annotate(total_quantity=Sum('quantiteVendu', output_field=IntegerField()))
        .order_by('-total_quantity')
        .first()
    )

    medicament_stats = (
        DetailVente.objects.values('id_Medicaments__nom')
        .annotate(total_quantity=Sum('quantiteVendu', output_field=IntegerField()))
        .order_by('-total_quantity')[:5]
    )

    top_sale = ventes.order_by('-totalVente').first()

    top_sales = ventes.values('dateVente', 'totalVente').order_by('dateVente')

    # Sérialiser les données en JSON
    top_sales_json = json.dumps(list(top_sales), default=str)
    medicament_stats_json = json.dumps(list(medicament_stats), default=str)

    return render(request, 'sales_dashboard.html', {
        'ventes': ventes,
        'total_revenue': total_revenue,
        'top_medicament': top_medicament,
        'medicament_stats': medicament_stats_json,  # Passer les données sérialisées
        'top_sales': top_sales_json,  # Passer les données sérialisées
        'top_sale': top_sale,
        'username': username,
        
    })


@login_required
@role_required('gestionnaire_ventes')
def ventes_index(request):
    username = request.user.username
    today = timezone.now().date()
    ventes = Vente.objects.filter(dateVente__date=today)
    return render(request, 'ventes/index.html', {'ventes': ventes, 'username': username})


@login_required
@role_required('gestionnaire_ventes')
def search_ventes(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        ventes = Vente.objects.filter(
            Q(id_User__username__icontains=query) |
            Q(dateVente__icontains=query) |
            Q(totalVente__icontains=query)
        ).values('id_Vente', 'id_User__username', 'dateVente', 'totalVente')
        return JsonResponse({'ventes': list(ventes)})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


@login_required
@role_required('gestionnaire_ventes')
def vente_detail(request, id):
    try:
        vente = Vente.objects.get(id_Vente=id)
        details = DetailVente.objects.filter(id_Vente=vente).select_related('id_Medicaments')
        
        details_list = []
        total_html = 0
        for detail in details:
            prix_unitaire = float(detail.sousTotal) / detail.quantiteVendu if detail.quantiteVendu > 0 else 0
            details_list.append({
                'medicament': detail.id_Medicaments.nom,
                'quantite': detail.quantiteVendu,
                'prix_unitaire': prix_unitaire,
                'total': float(detail.sousTotal)
            })
            total_html += float(detail.sousTotal)
        
        # Créer le contenu HTML pour le modal
        modal_content = f"""
        <div class="container">
            <div class="row mb-3">
                <div class="col">
                    <strong>Numéro de vente:</strong> {vente.id_Vente}
                </div>
                <div class="col">
                    <strong>Date:</strong> {vente.dateVente.strftime("%d/%m/%Y %H:%M")}
                </div>
            </div>
            <table class="table">
                <thead>
                    <tr>
                        <th>Médicament</th>
                        <th>Quantité</th>
                        <th>Prix unitaire</th>
                        <th>Total</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        for detail in details_list:
            modal_content += f"""
                    <tr>
                        <td>{detail['medicament']}</td>
                        <td>{detail['quantite']}</td>
                        <td>{detail['prix_unitaire']:.2f}</td>
                        <td>{detail['total']:.2f}</td>
                    </tr>
            """
        
        modal_content += f"""
                </tbody>
                <tfoot>
                    <tr>
                        <td colspan="3" class="text-right"><strong>Total</strong></td>
                        <td><strong>{total_html:.2f}</strong></td>
                    </tr>
                </tfoot>
            </table>
        </div>
        """
        
        return JsonResponse({
            'modal_content': modal_content,
            'vente_id': vente.id_Vente,
            'date_vente': vente.dateVente.strftime("%Y-%m-%d %H:%M:%S"),
            'total_vente': float(vente.totalVente),
            'details': details_list
        })
    except Vente.DoesNotExist:
        return JsonResponse({
            'error': 'Vente non trouvée'
        }, status=404)
    except Exception as e:
        logger.error(f"Erreur dans la vue vente_detail : {e}")
        return JsonResponse({
            'error': 'Une erreur est survenue lors de la récupération des détails de la vente.'
        }, status=500)


@login_required
@role_required('gestionnaire_ventes')
def filter_by_category(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        medicaments = Medicament.objects.filter(
            id_Categorie=category_id,
            stock__quantite__gt=0,
            est_cachee=False
        ).distinct().values('id_Medicament', 'nom', 'description', 'prixUnitaire', 'image')
        return JsonResponse({'medicaments': list(medicaments)})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


@login_required
@role_required('gestionnaire_ventes')
def search_medicaments(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        medicaments = Medicament.objects.filter(
            nom__icontains=query,
            stock__quantite__gt=0,
            est_cachee=False
        ).distinct().values('id_Medicament', 'nom', 'description', 'prixUnitaire', 'image')
        return JsonResponse({'medicaments': list(medicaments)})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


@login_required
@role_required('gestionnaire_ventes')
def add_to_cart(request):
    if request.method == 'POST':
        medicament_id = request.POST.get('medicament_id')
        medicament = get_object_or_404(Medicament, id_Medicament=medicament_id)
        return JsonResponse({'status': 'success', 'name': medicament.nom, 'price': str(medicament.prixUnitaire)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@login_required
@role_required('gestionnaire_ventes')
def check_stock(request):
    if request.method == 'POST':
        medicament_id = request.POST.get('medicament_id')
        quantite = int(request.POST.get('quantite', 0))

        try:
            stock = Stock.objects.get(medicament_id=medicament_id)
            if stock.quantite >= quantite:
                return JsonResponse({
                    'status': 'success',
                    'available': True,
                    'stock': stock.quantite,
                    'can_sell': quantite
                })
            elif stock.quantite > 0:
                return JsonResponse({
                    'status': 'warning',
                    'available': True,
                    'message': f'Stock insuffisant. Seuls {stock.quantite} unités sont disponibles. Voulez-vous continuer avec cette quantité ?',
                    'stock': stock.quantite,
                    'can_sell': stock.quantite
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'available': False,
                    'message': 'Stock épuisé pour ce médicament',
                    'stock': 0,
                    'can_sell': 0
                })
        except Stock.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'available': False,
                'message': 'Aucun stock disponible pour ce médicament',
                'stock': 0,
                'can_sell': 0
            })
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@login_required
@role_required('gestionnaire_ventes')
def finalize_sale(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})

    try:
        cart_data = json.loads(request.POST.get('cart', '[]'))
        
        if not cart_data:
            return JsonResponse({'status': 'error', 'message': 'Le panier est vide'})

        with transaction.atomic():
            total_vente = Decimal('0.00')
            vente = Vente.objects.create(
                totalVente=total_vente,
                dateVente=timezone.now(),
                id_User=request.user
            )
            
            for item in cart_data:
                medicament = Medicament.objects.select_for_update().get(id_Medicament=item['id'])
                stock = Stock.objects.select_for_update().get(medicament=medicament)
                
                if stock.quantite >= item['quantity']:
                    # Calculer le sous-total pour ce médicament
                    sous_total = Decimal(str(item['quantity'])) * Decimal(str(item['price']))
                    
                    # Créer le détail de la vente
                    DetailVente.objects.create(
                        id_Vente=vente,
                        id_Medicaments=medicament,
                        quantiteVendu=item['quantity'],
                        sousTotal=sous_total
                    )
                    
                    # Mettre à jour le total
                    total_vente += sous_total
                    
                    # Mettre à jour le stock
                    stock.quantite -= item['quantity']
                    stock.save()
                    
                    if stock.quantite <= stock.seuil_alerte:
                        if stock.quantite == 0:
                            medicament.est_vendu = False
                            medicament.save()
                        Notification.objects.create(
                            message=f"Stock bas pour {medicament.nom}: {stock.quantite} restants",
                            type_notification="alerte_stock"
                        )
                else:
                    # Annuler la transaction si le stock est insuffisant
                    raise ValidationError(f"Stock insuffisant pour {medicament.nom}")

            # Mettre à jour le total de la vente
            vente.totalVente = total_vente
            vente.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Vente finalisée avec succès',
                'vente_id': vente.id_Vente,
                'total': float(total_vente)
            })
            
    except ValidationError as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Format de panier invalide'
        })
    except Exception as e:
        logger.error(f"Erreur lors de la finalisation de la vente: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': 'Une erreur est survenue lors de la finalisation de la vente'
        })


@login_required
def check_auth(request):
    return JsonResponse({
        'authenticated': request.user.is_authenticated,
        'username': request.user.username if request.user.is_authenticated else None
    })
