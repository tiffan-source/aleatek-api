# Generated by Django 4.2 on 2023-06-08 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ouvrage', '0012_entrepriseaffaireouvrage_unique_entreprise_ouvrage'),
    ]

    operations = [
        migrations.AddField(
            model_name='affaireouvrage',
            name='diffusion',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='entrepriseaffaireouvrage',
            name='diffusion',
            field=models.BooleanField(default=False),
        ),
    ]
