# Generated by Django 5.1.4 on 2024-12-24 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Utilisateurs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilisateur',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
