# Generated by Django 4.2 on 2023-06-08 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ouvrage', '0013_affaireouvrage_diffusion_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='documents',
            name='traite',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]