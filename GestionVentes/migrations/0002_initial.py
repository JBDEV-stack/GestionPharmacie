# Generated by Django 5.1.4 on 2025-01-08 06:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('GestionVentes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='vente',
            name='id_User',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='detailvente',
            name='id_Vente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='GestionVentes.vente'),
        ),
    ]
