# Generated by Django 5.1.4 on 2025-01-08 06:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GestionStocks', '0002_rename_quantite_commander_commande_quantite_commande_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fournisseur',
            name='contact',
        ),
    ]
