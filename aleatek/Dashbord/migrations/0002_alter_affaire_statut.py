# Generated by Django 4.2 on 2023-06-01 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dashbord', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='affaire',
            name='statut',
            field=models.CharField(choices=[('En cours', 'En cours'), ('Achevé', 'Achevé'), ('Abandonné', 'Abandonné')], max_length=20),
        ),
    ]
