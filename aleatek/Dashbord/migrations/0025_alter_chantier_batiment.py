# Generated by Django 3.2.19 on 2023-06-17 09:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Dashbord', '0024_affaire_numero_contrat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chantier',
            name='batiment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Dashbord.batiment'),
        ),
    ]
