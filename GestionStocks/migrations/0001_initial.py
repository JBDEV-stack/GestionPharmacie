# Generated by Django 5.1.4 on 2024-12-13 03:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategorieMedicament',
            fields=[
                ('id_Categorie', models.AutoField(primary_key=True, serialize=False)),
                ('nom_Categorie', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Medicament',
            fields=[
                ('id_Medicament', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('prixUnitaire', models.DecimalField(decimal_places=2, max_digits=10)),
                ('code_barre', models.IntegerField()),
                ('id_Categorie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GestionStocks.categoriemedicament')),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id_Stock', models.AutoField(primary_key=True, serialize=False)),
                ('quantite', models.IntegerField()),
                ('seuil_alerte', models.IntegerField()),
                ('medicament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GestionStocks.medicament')),
            ],
        ),
    ]
